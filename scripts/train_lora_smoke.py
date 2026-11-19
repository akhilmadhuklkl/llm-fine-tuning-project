"""Run a one-step, minimum-resource LoRA training smoke test."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
import yaml
from peft import LoraConfig, TaskType, get_peft_model
from torch.utils.data import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer


class ChatDataset(Dataset):
    def __init__(self, path: Path, tokenizer, max_length: int):
        self.examples = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            if tokenizer.chat_template:
                text = tokenizer.apply_chat_template(record["messages"], tokenize=False)
            else:
                text = "\n".join(f"{message['role']}: {message['content']}" for message in record["messages"])
            encoded = tokenizer(text, truncation=True, max_length=max_length, padding="max_length")
            encoded["labels"] = list(encoded["input_ids"])
            self.examples.append({key: torch.tensor(value) for key, value in encoded.items()})

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, index):
        return self.examples[index]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/training.yaml")
    args = parser.parse_args()

    config = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    model_config = yaml.safe_load(Path(config["model_config"]).read_text(encoding="utf-8"))
    model_id = model_config["model_id"]
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(model_id)
    model.config.use_cache = False
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=config["lora_r"],
        lora_alpha=config["lora_alpha"],
        lora_dropout=config["lora_dropout"],
        target_modules=config["lora_target_modules"],
        bias="none",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    train_dataset = ChatDataset(Path(config["train_file"]), tokenizer, config["max_seq_length"])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config["learning_rate"])
    model.train()
    for step, batch in enumerate(train_dataset):
        if step >= config["max_steps"]:
            break
        batch = {key: value.unsqueeze(0).to(device) for key, value in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss / config["gradient_accumulation_steps"]
        loss.backward()
        if (step + 1) % config["gradient_accumulation_steps"] == 0 or step + 1 == config["max_steps"]:
            optimizer.step()
            optimizer.zero_grad()
        print(f"step={step + 1} loss={loss.item():.4f} device={device}")
    Path(config["output_dir"]).mkdir(parents=True, exist_ok=True)
    model.save_pretrained(config["output_dir"])
    print("LoRA smoke test completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

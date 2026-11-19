"""Run the selected base model on the baseline incident prompts."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import torch
import yaml
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel


def load_prompts(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def generate(model, tokenizer, messages: list[dict], max_new_tokens: int, prefix_allowed_tokens_fn=None) -> str:
    if tokenizer.chat_template:
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    else:
        prompt = "\n".join(f"{message['role']}: {message['content']}" for message in messages) + "\nassistant:"
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {key: value.to(model.device) for key, value in inputs.items()}
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            prefix_allowed_tokens_fn=prefix_allowed_tokens_fn,
        )
    generated = output[0][inputs["input_ids"].shape[1] :]
    return tokenizer.decode(generated, skip_special_tokens=True).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", default="evaluation/baseline_prompts.jsonl")
    parser.add_argument("--output", default="evaluation/baseline_results.jsonl")
    parser.add_argument("--max-new-tokens", type=int, default=256)
    parser.add_argument("--model-config", default="configs/model.yaml")
    parser.add_argument("--adapter-dir", default=None, help="Optional local LoRA adapter directory")
    parser.add_argument("--constrain-json", action="store_true", help="Constrain generation to the incident JSON schema")
    parser.add_argument("--allow-slow-cpu", action="store_true", help="Allow more than six prompts on CPU")
    args = parser.parse_args()

    config = yaml.safe_load(Path(args.model_config).read_text(encoding="utf-8"))
    model_id = config["model_id"]
    prompts = load_prompts(Path(args.prompts))
    if not torch.cuda.is_available() and len(prompts) > 6 and not args.allow_slow_cpu:
        raise RuntimeError(
            f"Large CPU evaluation is blocked for {len(prompts)} prompts. "
            "Use CUDA or pass --allow-slow-cpu only after accepting the resource cost."
        )
    print(f"Loading {model_id}...")
    tokenizer_kwargs = {"use_fast": True, "extra_special_tokens": {}}
    tokenizer = AutoTokenizer.from_pretrained(model_id, **tokenizer_kwargs)
    model = AutoModelForCausalLM.from_pretrained(model_id, device_map=config.get("device_map", "auto"))
    if args.adapter_dir:
        model = PeftModel.from_pretrained(model, args.adapter_dir)
        print(f"Loaded LoRA adapter: {args.adapter_dir}")
    model.eval()
    print(f"Running on: {model.device}")
    prefix_allowed_tokens_fn = None
    if args.constrain_json:
        from lmformatenforcer import JsonSchemaParser
        from lmformatenforcer.integrations.transformers import build_transformers_prefix_allowed_tokens_fn

        schema = {
            "type": "object",
            "properties": {
                "severity": {
                    "type": "string",
                    "enum": ["SEV-0", "SEV-1", "SEV-2", "SEV-3", "none", "unknown"],
                },
                "incident_type": {"type": "string"},
                "affected_services": {"type": "array", "maxItems": 3, "items": {"type": "string", "maxLength": 80}},
                "observed_facts": {"type": "array", "maxItems": 3, "items": {"type": "string", "maxLength": 160}},
                "hypotheses": {"type": "array", "maxItems": 3, "items": {"type": "string", "maxLength": 160}},
                "next_steps": {"type": "array", "maxItems": 3, "items": {"type": "string", "maxLength": 160}},
                "escalation_required": {"type": "boolean"},
            },
            "required": [
                "severity", "incident_type", "affected_services", "observed_facts",
                "hypotheses", "next_steps", "escalation_required",
            ],
        }
        prefix_allowed_tokens_fn = build_transformers_prefix_allowed_tokens_fn(
            tokenizer, JsonSchemaParser(schema)
        )
        print("JSON schema constraints: enabled")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output_file:
        for item in prompts:
            print(f"Generating {item['id']}...")
            response = generate(
                model, tokenizer, item["messages"], args.max_new_tokens, prefix_allowed_tokens_fn
            )
            result = {
                "id": item["id"],
                "category": item.get("category", "live_input"),
                "model_id": model_id,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "response": response,
            }
            output_file.write(json.dumps(result, ensure_ascii=False) + "\n")
            output_file.flush()
            print(response.encode("ascii", errors="backslashreplace").decode("ascii"))
            print()
    print(f"Saved baseline results to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

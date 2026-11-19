"""Create a tiny local GPT-2 model and tokenizer for pipeline tests."""

from __future__ import annotations

import json
from pathlib import Path

from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import Whitespace
from transformers import GPT2Config, GPT2LMHeadModel, PreTrainedTokenizerFast


def main() -> int:
    data_path = Path("data/processed/train_chat.jsonl")
    output_dir = Path("models/tiny-smoke-model")
    texts = []
    for line in data_path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        texts.extend(message["content"] for message in record["messages"])

    special_tokens = ["<pad>", "<unk>", "<bos>", "<eos>", "<system>", "<user>", "<assistant>"]
    vocabulary = {token: index for index, token in enumerate(special_tokens)}
    for text in texts:
        for token in text.split():
            if token not in vocabulary:
                vocabulary[token] = len(vocabulary)

    tokenizer_backend = Tokenizer(WordLevel(vocab=vocabulary, unk_token="<unk>"))
    tokenizer_backend.pre_tokenizer = Whitespace()
    tokenizer = PreTrainedTokenizerFast(
        tokenizer_object=tokenizer_backend,
        pad_token="<pad>",
        unk_token="<unk>",
        bos_token="<bos>",
        eos_token="<eos>",
    )
    tokenizer.save_pretrained(output_dir)

    config = GPT2Config(
        vocab_size=len(vocabulary),
        n_positions=256,
        n_ctx=256,
        n_embd=64,
        n_layer=2,
        n_head=2,
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
    model = GPT2LMHeadModel(config)
    model.save_pretrained(output_dir)
    print(f"Created tiny model with vocabulary size {len(vocabulary)} at {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

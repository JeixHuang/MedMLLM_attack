# src/transformer_utils/tokenizer.py
from transformers import AutoTokenizer

def load_tokenizer(path):
    return AutoTokenizer.from_pretrained(path)

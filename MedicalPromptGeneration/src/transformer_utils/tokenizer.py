from transformers import AutoTokenizer

def load_tokenizer(path):
    return AutoTokenizer.from_pretrained(path)

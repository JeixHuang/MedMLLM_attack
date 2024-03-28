import os

os.sys.path.append("..")
from configs.template import get_config as default_config

def get_config():
    
    config = default_config()
    config.model_paths = [
        "/home/huangxijie/llm-attack/DIR/vicuna/vicuna-tiny-1b",
    ]
    config.tokenizer_paths = [
        "/home/huangxijie/llm-attack/DIR/vicuna/vicuna-tiny-1b",
    ]

    return config

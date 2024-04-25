import json
import os

def load_config(config_file):
    config_path = os.path.join(os.path.dirname(__file__), '..', config_file)
    with open(config_path) as f:
        return json.load(f)

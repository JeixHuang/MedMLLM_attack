# src/main.py
import argparse
import json
from model import MedicalPromptModel

def main():
    parser = argparse.ArgumentParser(description="Run the medical prompt generation model.")
    parser.add_argument('--model_type', type=str, choices=['bert', 'ofa', 'vilt'], help='Select the model type to use.')
    args = parser.parse_args()

    with open('../configs/model_config.json') as f:
        config = json.load(f)

    model = MedicalPromptModel(config, args.model_type)
    # 这里可以继续添加更多的功能逻辑，例如训练、测试等

if __name__ == "__main__":
    main()

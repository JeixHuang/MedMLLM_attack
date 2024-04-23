# src/main.py
import json
from data_loader import DataLoader
from model import MedicalPromptModel

def main():
    with open('../configs/model_config.json') as f:
        config = json.load(f)

    data_loader = DataLoader(config)
    model = MedicalPromptModel(config)
    model.train(data_loader)

if __name__ == "__main__":
    main()

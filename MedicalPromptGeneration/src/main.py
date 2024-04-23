from src.model import MedicalPromptModel
from src.data_loader import DataLoader
import argparse
import json

def main(args):
    # Load configuration
    with open(args.config, 'r') as f:
        config = json.load(f)

    # Initialize the data loader
    data_loader = DataLoader(config)

    # Initialize the model
    model = MedicalPromptModel(config, data_loader)

    # Train or evaluate
    if args.mode == 'train':
        model.train()
    elif args.mode == 'test':
        model.evaluate()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Medical Prompt Generation')
    parser.add_argument('--config', type=str, default='configs/model_config.json', help='Path to config file')
    parser.add_argument('--mode', type=str, default='train', choices=['train', 'test'], help='Operation mode')
    args = parser.parse_args()
    main(args)

# src/main.py
import argparse
import json
from model import VQAModel
from PIL import Image
import os

def main():
    parser = argparse.ArgumentParser(description="Run VQA on a given image.")
    parser.add_argument('--image_path', type=str, help='Path to the image file.')
    parser.add_argument('--model_type', type=str, default='vilt', help='Model type to use for VQA.')
    args = parser.parse_args()

    config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'model_config.json')
    with open(config_path) as f:
        config = json.load(f)

    image = Image.open(args.image_path)

    # Assume the question is stored in an associated .txt file in the annotations directory
    base_image_name = os.path.basename(args.image_path).replace('.png', '.txt')
    annotation_path = os.path.join(os.path.dirname(args.image_path).replace('images', 'annotations'), base_image_name)

    with open(annotation_path, 'r') as file:
        question = file.read().strip()

    model = VQAModel(config, args.model_type)
    answer = model.answer_question(image, question)
    print("Predicted answer:", answer)

if __name__ == "__main__":
    main()

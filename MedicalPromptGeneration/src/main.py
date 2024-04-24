# src/main.py
import argparse
import json
from model import VQAModel
from PIL import Image
import os

def main():
    parser = argparse.ArgumentParser(description="Run VQA on given images and their corresponding questions.")
    parser.add_argument('--model_type', type=str, default='vilt', help='Model type to use for VQA.')
    args = parser.parse_args()

    config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'model_config.json')
    with open(config_path) as f:
        config = json.load(f)

    image_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'images')
    annotation_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'annotations')

    model = VQAModel(config, args.model_type)

    # Process each image and its corresponding annotation file
    for image_file in os.listdir(image_dir):
        if image_file.endswith('.png'):
            image_path = os.path.join(image_dir, image_file)
            image = Image.open(image_path)

            # Corresponding annotation file
            annotation_file = image_file.replace('.png', '.txt')
            annotation_path = os.path.join(annotation_dir, annotation_file)

            try:
                with open(annotation_path, 'r') as file:
                    questions = file.readlines()

                for question in questions:
                    question = question.strip()
                    if question:  # Ensure question is not empty
                        answer = model.answer_question(image, question)
                        print(f"Image: {image_file}, Question: {question}, Answer: {answer}")
            except FileNotFoundError:
                print(f"Annotation file not found for {image_file}")

if __name__ == "__main__":
    main()

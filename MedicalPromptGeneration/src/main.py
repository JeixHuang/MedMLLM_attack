import argparse
import os
from PIL import Image
from config_loader import load_config
from model_handler import initialize_model
from question_processor import process_questions

def main():
    parser = argparse.ArgumentParser(description="Generate a list of attributes from images using different VQA models.")
    args = parser.parse_args()

    config = load_config('configs/model_config.json')

    images_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'images')
    outputs_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'ret')

    # Create the outputs directory if it does not exist
    os.makedirs(outputs_dir, exist_ok=True)

    # Initialize models
    model_blip = initialize_model(config, 'blip')
    model_imv = initialize_model(config, 'IMV')

    # Process each image in the directory
    for image_file in os.listdir(images_dir):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
            image_path = os.path.join(images_dir, image_file)
            image = Image.open(image_path).convert('RGB')

            # Process questions with BLIP model using annotations from sample1.txt
            blip_answers = process_questions(model_blip, image, os.path.join(os.path.dirname(__file__), '..', 'data', 'annotations', 'univesal_attributes.txt'))

            # Process questions with IMV model using annotations from sample2.txt
            imv_answers = process_questions(model_imv, image, os.path.join(os.path.dirname(__file__), '..', 'data', 'annotations', 'medical_attributes.txt'))

            # Save the results in the outputs directory
            output_filename = os.path.splitext(image_file)[0] + '.txt'
            output_path = os.path.join(outputs_dir, output_filename)

            with open(output_path, 'w') as f:
                f.write(f"Attributes for image '{image_file}':\n")
                for answer in blip_answers + imv_answers:
                    f.write(f"Question: {answer['question']}\nAnswer: {answer['answer']}\n")

if __name__ == "__main__":
    main()

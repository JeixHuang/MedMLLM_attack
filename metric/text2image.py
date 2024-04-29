import argparse
import torch
from PIL import Image
import os
from transformers import CLIPProcessor, CLIPModel

from open_clip import create_model_from_pretrained, get_tokenizer

model, preprocess = create_model_from_pretrained('hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224')
tokenizer = get_tokenizer('hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224')

# Load the CLIP model and processor
model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')
processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
model.eval()

def get_clip_score(image_path, text):
    image = Image.open(image_path)
    inputs = processor(text=text, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    return logits_per_image.item()

def main():
    parser = argparse.ArgumentParser(description='Compare images with textual descriptions using CLIP.')
    parser.add_argument('--image_folder', type=str, default='./images', help='Folder containing images')
    parser.add_argument('--text_folder', type=str, default='./text', help='Folder containing text descriptions')
    args = parser.parse_args()

    image_directory = args.image_folder
    text_directory = args.text_folder

    test_imgs = [os.path.join(image_directory, f) for f in os.listdir(image_directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
    test_texts = [os.path.join(text_directory, f) for f in os.listdir(text_directory) if f.endswith('.txt')]

    img_to_text = {os.path.splitext(os.path.basename(img))[0]: os.path.join(text_directory, os.path.splitext(os.path.basename(img))[0] + '.txt') for img in test_imgs}

    for img_name, text_path in img_to_text.items():
        img_path = os.path.join(image_directory, img_name)
        if os.path.exists(img_path) and os.path.exists(text_path):
            with open(text_path, 'r') as file:
                text = file.read()
            score = get_clip_score(img_path, text)
            print(f"Image: {img_path}, Text: {text_path}, Similarity Score: {score}")
        else:
            print(f"Missing file for {img_name}: Image path {img_path} or text path {text_path} does not exist.")


if __name__ == '__main__':
    main()

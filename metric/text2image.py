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
    max_length = 2048  # Adjusted based on your model's configuration
    image = Image.open(image_path)
    inputs = processor(text=text[:max_length], images=image, return_tensors="pt", padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}  # Ensure all inputs are on the same device as the model
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    return logits_per_image.item()

def main():
    parser = argparse.ArgumentParser(description='Compare images with textual descriptions using CLIP.')
    parser.add_argument('--image_folder', type=str, default='./images', help='Folder containing images')
    parser.add_argument('--normal_text_folder', type=str, default='./output_normal', help='Folder containing normal text descriptions')
    parser.add_argument('--harmful_text_folder', type=str, default='./output_harmful', help='Folder containing harmful text descriptions')
    args = parser.parse_args()

    image_directory = args.image_folder
    normal_text_directory = args.normal_text_folder
    harmful_text_directory = args.harmful_text_folder

    # Load all images
    test_imgs = [os.path.join(image_directory, f) for f in os.listdir(image_directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    for img_file in test_imgs:
        base_name = os.path.splitext(os.path.basename(img_file))[0]
        normal_text_path = os.path.join(normal_text_directory, base_name + '.txt')
        harmful_text_path = os.path.join(harmful_text_directory, base_name + '.txt')

        if os.path.exists(img_file) and os.path.exists(normal_text_path) and os.path.exists(harmful_text_path):
            with open(normal_text_path, 'r') as file:
                normal_text = file.read()
            with open(harmful_text_path, 'r') as file:
                harmful_text = file.read()

            normal_score = get_clip_score(img_file, normal_text)
            harmful_score = get_clip_score(img_file, harmful_text)

            print(f"Image: {img_file}")
            print(f"Normal Text: {normal_text_path}, Similarity Score: {normal_score}")
            print(f"Harmful Text: {harmful_text_path}, Similarity Score: {harmful_score}")
        else:
            print(f"Missing files for {base_name}: Check paths for image and text files.")

if __name__ == '__main__':
    main()

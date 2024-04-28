import argparse
import torch
from PIL import Image
import matplotlib.pyplot as plt
import os
from transformers import CLIPProcessor, CLIPModel

from open_clip import create_model_from_pretrained, get_tokenizer # works on open-clip-torch>=2.23.0, timm>=0.9.8

model, preprocess = create_model_from_pretrained('hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224')
tokenizer = get_tokenizer('hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224')

# Constants and configurations
template = 'this is a photo of '
labels = [
    'adenocarcinoma histopathology', 'brain MRI', 'covid line chart',
    'squamous cell carcinoma histopathology', 'immunohistochemistry histopathology',
    'bone X-ray', 'chest X-ray', 'pie chart', 'hematoxylin and eosin histopathology'
]
image_directory = './images'
test_imgs = [os.path.join(image_directory, f) for f in os.listdir(image_directory) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Load the CLIP model and processor
model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')
processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
model.eval()

def preprocess_and_classify():
    images = [Image.open(img) for img in test_imgs]
    inputs = processor(images, return_tensors="pt", padding=True).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)
        sorted_indices = probs.argsort(dim=1, descending=True)

    return probs.cpu().numpy(), sorted_indices.cpu().numpy()

def display_results(probs, sorted_indices):
    for i, img in enumerate(test_imgs):
        print(f"{os.path.basename(img)} predictions:")
        for idx in sorted_indices[i, :3]:  # Display the top 3 predictions
            print(f"{labels[idx]}: {probs[i, idx] * 100:.2f}%")
        print('\n')

def plot_images_with_metadata(probs, sorted_indices):
    num_images = len(test_imgs)
    fig, axes = plt.subplots(nrows=num_images, ncols=1, figsize=(10, 10 * num_images))
    for i, img_path in enumerate(test_imgs):
        img = Image.open(img_path)
        ax = axes.flatten()[i]
        ax.imshow(img)
        ax.axis('off')
        top_labels = [f"{labels[idx]}: {probs[i, idx] * 100:.2f}%" for idx in sorted_indices[i, :3]]
        ax.set_title(f"{os.path.basename(img_path)}\n{' '.join(top_labels)}", fontsize=12)
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Image classification tasks')
    parser.add_argument('--task', choices=['classify', 'visualize'], help='Task to perform: classify or visualize')
    args = parser.parse_args()

    probs, sorted_indices = preprocess_and_classify()

    if args.task == 'classify':
        display_results(probs, sorted_indices)
    elif args.task == 'visualize':
        plot_images_with_metadata(probs, sorted_indices)

if __name__ == '__main__':
    main()

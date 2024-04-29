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
    # Assuming that each image should be evaluated against each label
    # Create a list of text prompts for each label and each image
    texts = [template + label for label in labels for _ in test_imgs]  # Repeat text for each image
    images = [Image.open(img) for img in test_imgs for _ in labels]  # Repeat each image for each label

    # Process images and texts together
    inputs = processor(text=texts, images=images, return_tensors="pt", padding=True).to(device)

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

# def plot_images_with_metadata(probs, sorted_indices):
#     num_images = len(test_imgs)
#     num_labels_per_image = len(labels)
#     output_dir = 'output_images'
#     os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

#     fig, axes = plt.subplots(nrows=num_images, ncols=1, figsize=(10, 10 * num_images))
#     for i, img_path in enumerate(test_imgs):
#         img = Image.open(img_path)
#         ax = axes if num_images == 1 else axes[i]
#         ax.imshow(img)
#         ax.axis('off')

#         valid_indices = [idx for idx in sorted_indices[i, :3] if idx < num_labels_per_image]
#         top_labels = [f"{labels[idx]}: {probs[i, idx] * 100:.2f}%" for idx in valid_indices]
#         title = f"{os.path.basename(img_path)}\n{' '.join(top_labels)}"
#         ax.set_title(title, fontsize=12)
        
#         # Print results to console
#         print(title)

    # plt.tight_layout()
    # # Save the complete figure
    # # figure_path = os.path.join(output_dir, 'classified_images.png')
    # plt.savefig(figure_path)
    # print(f"Saved the figure to {figure_path}")
    # plt.close(fig)  # Close the figure to free memory

    # Optionally, save individual images
    # for i, img_path in enumerate(test_imgs):
    #     img = Image.open(img_path)
    #     fig, ax = plt.subplots()
    #     ax.imshow(img)
    #     ax.axis('off')
    #     valid_indices = [idx for idx in sorted_indices[i, :3] if idx < num_labels_per_image]
    #     top_labels = [f"{labels[idx]}: {probs[i, idx] * 100:.2f}%" for idx in valid_indices]
    #     ax.set_title(f"{os.path.basename(img_path)}\n{' '.join(top_labels)}", fontsize=12)
    #     individual_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(img_path))[0]}_classified.png")
    #     plt.savefig(individual_path)
    #     plt.close(fig)  # Close the individual figure
    #     print(f"Saved individual image to {individual_path}")

def main():
    parser = argparse.ArgumentParser(description='Image classification tasks')
    parser.add_argument('--task', choices=['classify', 'visualize'], help='Task to perform: classify or visualize')
    args = parser.parse_args()

    probs, sorted_indices = preprocess_and_classify()

    if args.task == 'classify':
        display_results(probs, sorted_indices)


if __name__ == '__main__':
    main()

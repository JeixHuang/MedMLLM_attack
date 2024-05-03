import argparse
import os
import time
import torch
from PIL import Image
import open_clip

# Load the CLIP model with open_clip
model, preprocess, _ = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
tokenizer = open_clip.get_tokenizer('ViT-B-32')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
model.eval()

def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"函数 {func.__name__} 运行时间：{end_time - start_time} 秒")
        return result
    return wrapper

@time_decorator
def get_clip_score(image_path, text):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    text_tokens = tokenizer([text], truncate=True).to(device)
    with torch.no_grad(), torch.cuda.amp.autocast():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text_tokens)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        text_probs = (100.0 * image_features @ text_features.T).softmax(dim=-1)
    return text_probs.max().item()

def main():
    parser = argparse.ArgumentParser(description='Compare images with textual descriptions using CLIP.')
    parser.add_argument('--image_folder', type=str, default='./images', help='Folder containing images')
    parser.add_argument('--normal_text_folder', type=str, default='./output_normal', help='Folder containing normal text descriptions')
    parser.add_argument('--harmful_text_folder', type=str, default='./output_harmful', help='Folder containing harmful text descriptions')
    args = parser.parse_args()

    image_directory = args.image_folder
    normal_text_directory = args.normal_text_folder
    harmful_text_directory = args.harmful_text_folder

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

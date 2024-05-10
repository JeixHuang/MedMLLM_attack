from datasets import load_dataset
import csv
import torch
from open_clip import create_model_from_pretrained, get_tokenizer
import random
from collections import OrderedDict
import time
import argparse
from typing import Any, List, Tuple
import os
import open_clip

# 这里导入IMAGENET2012_CLASSES
from classes import IMAGENET2012_CLASSES
label_to_id = {index: label for index, label in enumerate(IMAGENET2012_CLASSES.keys())}

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function '{func.__name__}' executed in {end - start:.4f} seconds.")
        return result
    return wrapper

@timing_decorator
def clip_score(model, image, tokenized_text) -> float:
    with torch.no_grad():
        image_features, text_features, logit_scale = model(image, tokenized_text)
        score = (logit_scale * image_features @ text_features.t()).detach()
    return score.item()

def process_split(split: str, device: torch.device, model: Any, preprocess: Any, tokenizer: Any) -> List[Tuple]:
    dataset = load_dataset("imagenet-1k", split=split)
    results = []
    all_labels = list(IMAGENET2012_CLASSES.values())

    for index, example in enumerate(dataset):
        label_id = label_to_id[example['label']]  # 从标签索引到类别ID的映射
        label_original = IMAGENET2012_CLASSES[label_id]
        unmatch_label = random.choice([l for l in all_labels if l != label_original])

        tokenized_text_original = tokenizer([f"this is a photo of {label_original}"]).to(device)
        tokenized_text_unmatch = tokenizer([f"this is a photo of {unmatch_label}"]).to(device)
        image = torch.stack([preprocess(example['image'])]).to(device)
        assert image.shape[-2:] == (224, 224)

        origin_score = clip_score(model, image, tokenized_text_original)
        unmatch_score = clip_score(model, image, tokenized_text_unmatch)

        results.append((index, label_original, origin_score, unmatch_label, unmatch_score))
        print(f"Processed {split} split, index {index}")

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate image-text similarity using a pretrained ViT-B model.")
    parser.add_argument("--split", default="train", type=str, help="Dataset split to process ('train', 'test', etc.)")
    parser.add_argument("--device", default="0", type=str, help="CUDA device ('cuda:0', 'cuda:1', etc.)")
    args = parser.parse_args()

    device = torch.device(f"cuda:{args.device}")
    model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-16', pretrained='openai')
    tokenizer = open_clip.get_tokenizer('ViT-B-16')
    model.to(device)
    model.eval()
    print("Model and tokenizer loaded successfully.")

    results = process_split(args.split, device, model, preprocess, tokenizer)

    results_dir = "metric/na2na_nature_img2text"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)  

    results_file = f"{results_dir}/{args.split}_results.csv"


    with open(results_file, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "label_original", "origin_score", "label_unmatch", "unmatch_score"])
        writer.writerows(results)

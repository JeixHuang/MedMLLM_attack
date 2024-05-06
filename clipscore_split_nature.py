from datasets import load_dataset
import csv
import torch
from open_clip import create_model_from_pretrained, get_tokenizer
import random
from collections import OrderedDict
import time
import argparse
from typing import Any, List, Tuple
import multiprocessing
from multiprocessing import Pool

# 这里导入IMAGENET2012_CLASSES
from classes import IMAGENET2012_CLASSES

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


def process_sample(index, example, all_labels, device, model, preprocess, tokenizer) -> Tuple:
    label_original = IMAGENET2012_CLASSES[example["label"]]
    unmatch_label = random.choice([l for l in all_labels if l != label_original])

    tokenized_text_original = tokenizer([f"this is a photo of {label_original}"]).to(
        device
    )
    tokenized_text_unmatch = tokenizer([f"this is a photo of {unmatch_label}"]).to(
        device
    )
    image = torch.stack([preprocess(example["image"])]).to(device)
    assert image.shape[-2:] == (224, 224)

    origin_score = clip_score(model, image, tokenized_text_original)
    unmatch_score = clip_score(model, image, tokenized_text_unmatch)

    return index, image, label_original, origin_score, unmatch_label, unmatch_score


def process_split_multiprocess(split: str, device: torch.device, model: Any, preprocess: Any, tokenizer: Any) -> List[Tuple]:

    results = []
    all_labels = list(IMAGENET2012_CLASSES.values())
    dataset = load_dataset("imagenet-1k", trust_remote_code=True, num_proc=10)

    with Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.starmap(
            process_sample,
            [
                (index, example, all_labels, device, model, preprocess, tokenizer)
                for index, example in enumerate(dataset[split])
            ],
        )

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate image-text similarity using a pretrained BiomedCLIP model.")
    parser.add_argument("--split", default="train", type=str, help="Dataset split to process ('train', 'test', etc.)")
    parser.add_argument("--device", default="0", type=str, help="CUDA device ('cuda:0', 'cuda:1', etc.)")

    args = parser.parse_args()

    device = torch.device(f"cuda:{args.device}")
    model_name = "hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224"
    tokenizer_name = "hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224"
    model, preprocess = create_model_from_pretrained(model_name)
    tokenizer = get_tokenizer(tokenizer_name)
    model.to(device)
    model.eval()
    print("Model and tokenizer loaded successfully.")

    results = process_split_multiprocess(
        args.split, device, model, preprocess, tokenizer
    )

    with open(f"nature_img2text/{args.split}_results.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "image", "label_original", "origin_score", "label_unmatch", "unmatch_score"])
        writer.writerows(results)

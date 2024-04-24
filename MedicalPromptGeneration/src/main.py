import argparse
import json
from model import VQAModel
from PIL import Image
import os
from transformers import BertTokenizer, BertModel
import torch
import spacy

# 加载spaCy的英文模型和BERT模型
nlp = spacy.load("en_core_web_sm")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def process_questions(model_vqa, image, questions):
    answers = []
    for question in questions:
        question = question.strip()
        if question:
            answer = model_vqa.answer_question(image, question)
            answers.append({"question": question, "answer": answer})
    return answers

def extract_relevant_keywords(text, main_subjects):
    # 使用BERT进行语义分析
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    last_hidden_states = outputs.last_hidden_state
    words = tokenizer.tokenize(text)
    
    # 提取与主题相关的关键词
    relevant_keywords = []
    for idx, word in enumerate(words):
        if any(subj in word for subj in main_subjects):
            relevant_keywords.append(word)
    return relevant_keywords

def main():
    parser = argparse.ArgumentParser(description="Generate a list of attributes from images using different VQA models.")
    args = parser.parse_args()

    config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'model_config.json')
    with open(config_path) as f:
        config = json.load(f)

    image_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'images', 'sample.png')
    annotation_path1 = os.path.join(os.path.dirname(__file__), '..', 'data', 'annotations', 'sample1.txt')
    annotation_path2 = os.path.join(os.path.dirname(__file__), '..', 'data', 'annotations', 'sample2.txt')

    image = Image.open(image_path).convert('RGB')

    # Process questions with BLIP model
    model_blip = VQAModel(config, 'blip')
    with open(annotation_path1, 'r') as file:
        questions = file.readlines()
    blip_answers = process_questions(model_blip, image, questions)

    # Process questions with IMV model
    model_imv = VQAModel(config, 'IMV')
    with open(annotation_path2, 'r') as file:
        questions = file.readlines()
    imv_answers = process_questions(model_imv, image, questions)

    # 主题词
    main_subjects = ['medical', 'image', 'color', 'size', 'shape', 'position']

    # Extract and filter keywords using BERT
    extracted_info = []
    for answer in blip_answers + imv_answers:
        keywords = extract_relevant_keywords(answer['answer'], main_subjects)
        extracted_info.extend(keywords)

    output_path = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'ret.txt')
    with open(output_path, 'w') as f:
        f.write(f"Attributes for image '{os.path.basename(image_path)}':\n")
        f.write(", ".join(set(extracted_info)))  # 使用 set 来去除重复的关键词

    print(f"Attributes for image '{os.path.basename(image_path)}':")
    print(", ".join(set(extracted_info)))

if __name__ == "__main__":
    main()

import argparse
import json
from model import VQAModel
from PIL import Image
import os
import spacy

# 加载spaCy的英文模型
nlp = spacy.load("en_core_web_sm")

def process_questions(model, image, questions):
    answers = []
    for question in questions:
        question = question.strip()
        if question:
            answer = model.answer_question(image, question)
            answers.append({"question": question, "answer": answer})
    return answers

def extract_nouns_and_adjectives(text):
    # 使用spaCy提取名词和形容词
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ']]
    return keywords

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

    # Extract keywords and save
    extracted_info = []
    for answer in blip_answers + imv_answers:
        keywords = extract_nouns_and_adjectives(answer['answer'])
        extracted_info.extend(keywords)

    output_path = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'ret.txt')
    with open(output_path, 'w') as f:
        f.write(f"Attributes for image '{os.path.basename(image_path)}':\n")
        f.write("\n".join(set(extracted_info)))  # 使用 set 来去除重复的关键词

    print(f"Attributes for image '{os.path.basename(image_path)}':")
    print("\n".join(set(extracted_info)))

if __name__ == "__main__":
    main()

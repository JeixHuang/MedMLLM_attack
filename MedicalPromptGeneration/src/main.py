import argparse
import json
from model import VQAModel
from PIL import Image
import os
import re

def process_questions(model, image, questions):
    answers = []
    for question in questions:
        question = question.strip()
        if question:
            answer = model.answer_question(image, question)
            answers.append({"question": question, "answer": answer})
    return answers

def extract_keywords(text):
    # 这里使用了简单的正则表达式来匹配名词短语作为关键词，这个方法可以根据需要进行更复杂的改进
    keywords = re.findall(r'\b\w+\b', text)
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
    keywords = []
    for answer in blip_answers + imv_answers:
        keywords.extend(extract_keywords(answer['answer']))

    output_path = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'ret.txt')
    with open(output_path, 'w') as f:
        f.write("\n".join(keywords))

    print("\n".join(keywords))

if __name__ == "__main__":
    main()

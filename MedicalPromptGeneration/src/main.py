import argparse
import json
from model import VQAModel
from PIL import Image
import os
from transformers import pipeline

def process_questions(model, image, questions):
    answers = []
    for question in questions:
        question = question.strip()
        if question:
            answer = model.answer_question(image, question)
            answers.append({"question": question, "answer": answer})
    return answers

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

    # Combine answers
    combined_answers = blip_answers + imv_answers

    # Prepare document QA pipeline
    nlp = pipeline("document-question-answering", model="naver-clova-ix/donut-base-finetuned-docvqa", tokenizer="naver-clova-ix/donut-base-finetuned-docvqa")

    # Extract relevant information
    extracted_info = []
    for answer_dict in combined_answers:
        response = nlp(answer_dict["answer"], answer_dict["question"])
        extracted_info.append(response["answer"])

    # Save and print the results
    output_path = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'ret.txt')
    with open(output_path, 'w') as f:
        for info in extracted_info:
            f.write(info + "\n")

    print("\n".join(extracted_info))

if __name__ == "__main__":
    main()

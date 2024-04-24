import argparse
import json
from model import VQAModel
from PIL import Image
import os
import torch
from transformers import DonutProcessor, VisionEncoderDecoderModel

def process_questions(model, image, questions):
    answers = []
    for question in questions:
        question = question.strip()
        if question:
            answer = model.answer_question(image, question)
            answers.append(f"Question: {question}\nAnswer: {answer}\n")
    return answers

def extract_info_with_donut(processor, model, device, answer_texts):
    extracted_info = []
    for text in answer_texts:
        # Prepare inputs for Donut
        task_prompt = "<s_docvqa><s_question>{}</s_question><s_answer>".format(text)
        decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids
        # Assume pixel_values are coming from a virtual image representation of text
        pixel_values = torch.randn(1, 3, 224, 224)  # Random noise as placeholder
        outputs = model.generate(
            pixel_values.to(device),
            decoder_input_ids=decoder_input_ids.to(device),
            max_length=model.decoder.config.max_position_embeddings,
            pad_token_id=processor.tokenizer.pad_token_id,
            eos_token_id=processor.tokenizer.eos_token_id,
            use_cache=True,
            bad_words_ids=[[processor.tokenizer.unk_token_id]],
            return_dict_in_generate=True,
        )
        sequence = processor.tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
        extracted_info.append(sequence)
    return extracted_info

def main():
    parser = argparse.ArgumentParser(description="Generate a list of attributes from images using different VQA models.")
    args = parser.parse_args()

    config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'model_config.json')
    with open(config_path) as f:
        config = json.load(f)

    image_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'images', 'sample.png')
    image = Image.open(image_path).convert('RGB')

    model_blip = VQAModel(config, 'blip')
    model_imv = VQAModel(config, 'IMV')

    # Load questions and process
    blip_answers = process_questions(model_blip, image, open(os.path.join(os.path.dirname(__file__), '..', 'data', 'annotations', 'sample1.txt')).readlines())
    imv_answers = process_questions(model_imv, image, open(os.path.join(os.path.dirname(__file__), '..', 'data', 'annotations', 'sample2.txt')).readlines())

    # Extract info using Donut model
    processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
    model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    extracted_info = extract_info_with_donut(processor, model, device, blip_answers + imv_answers)

    # Save and print the results
    output_path = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'ret.txt')
    with open(output_path, 'w') as f:
        f.writelines(extracted_info)
        print('\n'.join(extracted_info))

if __name__ == "__main__":
    main()

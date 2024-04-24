# src/model.py
from transformers import pipeline, AutoProcessor, AutoModelForPreTraining
from transformer_utils.model_utils import load_model, load_processor
from transformers import BlipProcessor, BlipForConditionalGeneration  # 导入BLIP模型专用类
import torch
from transformers import BlipProcessor, BlipForQuestionAnswering
import torch

class VQAModel:
    def __init__(self, config, model_type):
        self.model_type = model_type
        self.config = config

        if model_type == 'medical_ner':
            self.pipeline = pipeline("token-classification", model=config[f'{model_type}_path'], aggregation_strategy='simple')
        elif model_type == 'IMV':
            self.processor = AutoProcessor.from_pretrained(config['IMV_processor_path'])
            self.model = AutoModelForPreTraining.from_pretrained(config['IMV_model_path'])
        elif model_type == 'blip':
            # 使用正确的类初始化 BLIP 模型和处理器
            self.processor = BlipProcessor.from_pretrained(config['blip_path'])
            self.model = BlipForQuestionAnswering.from_pretrained(config['blip_path']).to('cuda')
        else:
            self.processor = load_processor(model_type, config[f'{model_type}_path'])
            self.model = load_model(model_type, config[f'{model_type}_path']).to('cuda')

    def answer_question(self, image, question):
        if self.model_type == 'medical_ner':
            return self.pipeline(question)
        elif self.model_type == 'IMV':
            inputs = self.processor([image, f"Question: {question}", "Answer:"], return_tensors="pt").to('cuda')
            outputs = self.model.generate(**inputs, max_new_tokens=50)
            answer = self.processor.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return answer
        elif self.model_type == 'blip':
            # 调整BLIP的使用方式，确保其通过生成方式返回答案
            inputs = self.processor(images=image, text=question, return_tensors="pt", padding=True).to('cuda')
            outputs = self.model.generate(**inputs, max_length=50)  # 指定最大长度限制
            answer = self.processor.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return answer
        else:
            inputs = self.processor(image, question, return_tensors="pt").to('cuda')
            outputs = self.model(**inputs)
            logits = outputs.logits
            idx = logits.argmax(-1).item()
            return self.model.config.id2label[idx]
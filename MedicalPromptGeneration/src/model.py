# src/model.py
from transformers import pipeline
from transformer_utils.model_utils import load_model, load_processor
import torch
from transformers import AutoProcessor, AutoModelForPreTraining
class VQAModel:
    def __init__(self, config, model_type):
        self.model_type = model_type
        self.config = config

        if model_type == 'medical_ner':
            # Initialize the NER pipeline directly for the medical NER model
            self.pipeline = pipeline("token-classification", model=config[f'{model_type}_path'], aggregation_strategy='simple')
        elif self.model_type == 'IMV':
            # 根据IMV模型需要加载对应的processor和model
            self.processor = AutoProcessor.from_pretrained(config['IMV_processor_path'])
            self.model = AutoModelForPreTraining.from_pretrained(config['IMV_model_path']).to('cuda')
        else:
            # 对于其他模型，使用通用的加载函数
            self.processor = load_processor(model_type, config[f'{model_type}_path'])
            self.model = load_model(model_type, config[f'{model_type}_path']).to('cuda')

    def answer_question(self, image, question):
        if self.model_type == 'medical_ner':
            # Directly use pipeline for text processing
            return self.pipeline(question)
        elif self.model_type == 'IMV':
            # 假设IMV模型需要特定格式的输入
            inputs = self.processor([image, f"Question: {question}", "Answer:"], return_tensors="pt").to('cuda')
            outputs = self.model(**inputs)
            # 假设使用生成方法或其他特定方法提取答案
            return outputs
        else:
            # 其他模型的处理
            inputs = self.processor(image, question, return_tensors="pt").to('cuda')
            outputs = self.model(**inputs)
            logits = outputs.logits
            idx = logits.argmax(-1).item()
            return self.model.config.id2label[idx]

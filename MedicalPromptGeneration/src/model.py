# src/model.py
from transformers import pipeline, AutoProcessor, AutoModelForPreTraining
from transformer_utils.model_utils import load_model, load_processor
import torch
class VQAModel:
    def __init__(self, config, model_type):
        self.model_type = model_type
        self.config = config

        if model_type == 'medical_ner':
            # 初始化医学命名实体识别模型的pipeline
            self.pipeline = pipeline("token-classification", model=config[f'{model_type}_path'], aggregation_strategy='simple')
        elif model_type == 'IMV':
            # 加载IMV模型，不立即移动至cuda
            self.processor = AutoProcessor.from_pretrained(config['IMV_processor_path'])
            self.model = AutoModelForPreTraining.from_pretrained(config['IMV_model_path'])
            if hasattr(self.model, 'requires_bitsandbytes'):
                self.requires_bitsandbytes = True
            else:
                self.requires_bitsandbytes = False
                # self.model.to('cuda')
        else:
            # 对于其他模型类型，使用通用的加载方法
            self.processor = load_processor(model_type, config[f'{model_type}_path'])
            self.model = load_model(model_type, config[f'{model_type}_path']).to('cuda')

    def answer_question(self, image, question):
        if self.model_type == 'medical_ner':
            # 使用pipeline直接处理文本
            return self.pipeline(question)
        elif self.model_type == 'IMV':
            # 处理IMV模型的输入
            inputs = self.processor([image, f"Question: {question}", "Answer:"], return_tensors="pt")
            if self.requires_bitsandbytes:
                outputs = self.model.generate(**inputs, max_new_tokens=50)  # 使用生成方法获取答案
            else:
                inputs = {k: v.to('cuda') for k, v in inputs.items()}
                outputs = self.model.generate(**inputs, max_new_tokens=50)  # 使用生成方法获取答案
            answer = self.processor.tokenizer.decode(outputs[0], skip_special_tokens=True)  # 解码生成的答案
            return answer
        else:
            # 处理其他模型类型的输入
            inputs = self.processor(image, question, return_tensors="pt").to('cuda')
            outputs = self.model(**inputs)
            logits = outputs.logits
            idx = logits.argmax(-1).item()
            return self.model.config.id2label[idx]

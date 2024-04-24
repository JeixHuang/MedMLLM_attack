# src/model.py
from transformer_utils.model_utils import load_model, load_processor
import torch

class VQAModel:
    def __init__(self, config, model_type):
        self.model_type = model_type
        self.processor = load_processor(model_type, config[f'{model_type}_path'])
        self.model = load_model(model_type, config[f'{model_type}_path'])

    def answer_question(self, image, question):
        inputs = self.processor(image, question, return_tensors="pt").to("cuda")
        if self.model_type in ['blip']:  # BLIP model uses generate
            output = self.model.generate(**inputs)
            return self.processor.decode(output[0], skip_special_tokens=True)
        else:  # Other models use logits
            outputs = self.model(**inputs)
            logits = outputs.logits
            idx = logits.argmax(-1).item()
            return self.model.config.id2label[idx]

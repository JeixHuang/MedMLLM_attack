# src/model.py
from transformer_utils.model_utils import load_model, load_processor

class VQAModel:
    def __init__(self, config, model_type):
        self.processor = load_processor(model_type, config[f'{model_type}_path'])
        self.model = load_model(model_type, config[f'{model_type}_path'])

    def answer_question(self, image, question):
        encoding = self.processor(image, question, return_tensors="pt")
        outputs = self.model(**encoding)
        logits = outputs.logits
        idx = logits.argmax(-1).item()
        return self.model.config.id2label[idx]

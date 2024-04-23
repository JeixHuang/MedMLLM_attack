# src/model.py
from transformer_utils.model_utils import load_model, load_processor

class MedicalPromptModel:
    def __init__(self, config, model_type):
        if model_type == 'vilt':
            self.processor = load_processor(model_type, config[f'{model_type}_path'])
            self.model = load_model(model_type, config[f'{model_type}_path'])
        else:
            self.model = load_model(model_type, config[f'{model_type}_path'])

    # 添加更多方法，如 train, test 等

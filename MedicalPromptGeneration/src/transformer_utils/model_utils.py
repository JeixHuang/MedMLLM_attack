# src/transformer_utils/model_utils.py
from transformers import AutoModel, ViltProcessor, ViltForQuestionAnswering

def load_model(model_type, model_path):
    if model_type == 'bert' or model_type == 'ofa':
        return AutoModel.from_pretrained(model_path)
    elif model_type == 'vilt':
        return ViltForQuestionAnswering.from_pretrained(model_path)
    else:
        raise ValueError("Unsupported model type")

def load_processor(model_type, model_path):
    if model_type == 'vilt':
        return ViltProcessor.from_pretrained(model_path)
    else:
        raise ValueError("Unsupported model type")

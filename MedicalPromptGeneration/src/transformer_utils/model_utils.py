from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

def load_model(model_type, model_path):
    if model_type == 'blip':
        return BlipForQuestionAnswering.from_pretrained(model_path).to("cuda")
    elif model_type == 'medical_ner':
        return AutoModelForTokenClassification.from_pretrained(model_path)
    else:
        raise ValueError("Unsupported model type")

def load_processor(model_type, model_path):
    if model_type == 'blip':
        return BlipProcessor.from_pretrained(model_path)
    elif model_type == 'medical_ner':
        return AutoTokenizer.from_pretrained(model_path)
    else:
        raise ValueError("Unsupported model type")

def load_pipeline(model_type, model_path):
    if model_type == 'medical_ner':
        return pipeline("token-classification", model=model_path, aggregation_strategy='simple')
    else:
        raise ValueError("Unsupported pipeline type for model")

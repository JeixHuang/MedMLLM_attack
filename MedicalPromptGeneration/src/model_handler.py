from model import VQAModel
from PIL import Image
import os

def initialize_model(config, model_type):
    return VQAModel(config, model_type)

def load_image(image_file):
    image_path = os.path.join(os.path.dirname(__file__), '..', image_file)
    return Image.open(image_path).convert('RGB')

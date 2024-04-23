# src/data_loader.py
from torch.utils.data import DataLoader, Dataset
import os
from PIL import Image

class MedicalDataset(Dataset):
    def __init__(self, image_dir, annotation_dir):
        self.images = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.endswith('.png')]
        self.annotation_dir = annotation_dir

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = self.images[idx]
        img = Image.open(img_path).convert('RGB')
        annotation_path = os.path.join(self.annotation_dir, os.path.basename(img_path).replace('.png', '.txt'))
        with open(annotation_path, 'r') as file:
            annotation = file.read()
        return img, annotation

def DataLoader(config):
    dataset = MedicalDataset(config['image_data_path'], config['annotation_data_path'])
    return DataLoader(dataset, batch_size=config['batch_size'], shuffle=True)

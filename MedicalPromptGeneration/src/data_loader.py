from torch.utils.data import DataLoader, Dataset
from PIL import Image
import os

class MedicalDataset(Dataset):
    def __init__(self, image_dir, annotation_dir):
        self.image_dir = image_dir
        self.annotation_dir = annotation_dir
        self.images = os.listdir(image_dir)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_name = self.images[idx]
        img_path = os.path.join(self.image_dir, img_name)
        img = Image.open(img_path).convert('RGB')
        # Assume annotations are in a separate file or format
        annotation_path = os.path.join(self.annotation_dir, img_name.replace('.png', '.txt'))
        with open(annotation_path, 'r') as file:
            annotation = file.read()
        return img, annotation

def DataLoader(config):
    dataset = MedicalDataset(config['image_data_path'], config['annotation_data_path'])
    return DataLoader(dataset, batch_size=config['batch_size'], shuffle=True)

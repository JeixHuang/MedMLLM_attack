import os
import json
from torchvision import transforms
from PIL import Image
from torch.utils.data import Dataset, DataLoader

class MedicalImageDataset(Dataset):
    def __init__(self, data_path, transform=None):
        self.data_path = data_path
        self.transform = transform
        self.images = [os.path.join(data_path, f) for f in os.listdir(data_path) if f.endswith('.jpg')]

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image_path = self.images[idx]
        image = Image.open(image_path)
        if self.transform:
            image = self.transform(image)
        return image

def make_dataloader(config):
    transform = transforms.Compose([
        transforms.Resize((384, 384)),
        transforms.ToTensor()
    ])
    dataset = MedicalImageDataset(config['data_path'], transform=transform)
    dataloader = DataLoader(dataset, batch_size=config['batch_size'], shuffle=True)
    return dataloader

import os 
import pandas as pd
import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image

class LesionDataset(torch.utils.data.Dataset):
    def __init__(self, img_dir, labels_fname, train_mode, test_mode, augment=False):
        """
        Args:
            img_dir (str): Directory with all the images.
            labels_fname (str): Path to the csv file with labels.
        """
        self.img_dir = img_dir
        self.labels = pd.read_csv(labels_fname)
    
        # Data Augmentation
        self.augment = transforms.Compose([
            transforms.RandomHorizontalFlip(0.5),
            transforms.RandomVerticalFlip(0.5),
            transforms.RandomRotation(60),
            transforms.ColorJitter(brightness=0.4, contrast=0.1, saturation=0.05, hue=0.05),
            transforms.RandomPerspective(),
            transforms.RandomInvert()
        ])

        self.train_transforms = transforms.Compose([
                                transforms.Resize(224),
                                transforms.RandomCrop(224),
                                transforms.ToTensor(),
                                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                     std=[0.229, 0.224, 0.225])
                            ])
        self.test_transforms = transforms.Compose([
                               transforms.Resize(224),
                               transforms.CenterCrop(224),
                               transforms.ToTensor(),
                               transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                     std=[0.229, 0.224, 0.225])
                            ])     
                            
        self.train_mode = train_mode
        self.test_mode = test_mode

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        img_name = self.labels.iloc[idx, 0]
        img_path = os.path.join(self.img_dir, f"{img_name}.jpg")
        image = Image.open(img_path)

        if self.train_mode:
            image = self.train_transforms(image)
            if self.augment:
                image = self.augment(image)
        elif self.test_mode:
            image = self.test_transforms(image)
    
        label = np.argmax(self.labels.iloc[idx, 1:])

        return image, label

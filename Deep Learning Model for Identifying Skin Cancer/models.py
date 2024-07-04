import torch
import torch.nn as nn
import torchvision

# Implement a SimpleBNConv

class SimpleBNConv(nn.Module):
    def __init__(self):
        super().__init__()
        # Initialise a Sequential module
        self.seq = nn.Sequential(
            nn.Conv2d(3, 8, 3), 
	        nn.ReLU(), 
            nn.BatchNorm2d(8), 
	        nn.MaxPool2d(2),

            nn.Conv2d(8, 16, 3), 
	        nn.ReLU(), 
            nn.BatchNorm2d(16), 
	        nn.MaxPool2d(2), 

            nn.Conv2d(16, 32, 3), 
	        nn.ReLU(), 
            nn.BatchNorm2d(32), 
	        nn.MaxPool2d(2), 

            nn.Conv2d(32, 64, 3), 
	        nn.ReLU(),
            nn.BatchNorm2d(64), 
	        nn.MaxPool2d(2),

            nn.Conv2d(64, 128, 3), 
	        nn.ReLU(), 
            nn.BatchNorm2d(128), 
	        nn.MaxPool2d(2),

            nn.Flatten(),
            nn.Linear(128*5*5, 32),
            nn.ReLU(),
            nn.Linear(32, 7)
        )

    def forward(self, x):
        return self.seq(x)
    

# Create a model from a pre-trained model from the torchvision model zoo.

def construct_resnet152():

    # Download the pre-trained model
    resnet152 = torchvision.models.resnet152(weights="IMAGENET1K_V2")

    # Fine tune all the weights
    for param in resnet152.parameters():
      param.requires_grad = True

    # Replace the final linear layer
    resnet152.fc = nn.Linear(2048, 7)

    return resnet152

# Create our own models

class EnhancedBNConv(nn.Module):
    def __init__(self):
        super().__init__()
        self.seq = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1), 
            nn.ReLU(),
            nn.BatchNorm2d(16),
            nn.MaxPool2d(2),

            nn.Conv2d(16, 32, 3, padding=1),  
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, padding=1), 
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, 3, padding=1),  
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.MaxPool2d(2),

            nn.Conv2d(128, 256, 3, padding=1),  
            nn.ReLU(),
            nn.BatchNorm2d(256),
            nn.MaxPool2d(2),

            nn.Conv2d(256, 512, 3, padding=1),  # Additional convolutional layer
            nn.ReLU(),
            nn.BatchNorm2d(512),
            nn.MaxPool2d(2),

            nn.Conv2d(512, 1024, 3, padding=1),  # Additional convolutional layer
            nn.ReLU(),
            nn.BatchNorm2d(1024),
            nn.MaxPool2d(2),

            nn.Flatten(),
            nn.Linear(1024 * 1 * 1, 256),  
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 7)  
        )
        
    def forward(self, x):
        return self.seq(x)





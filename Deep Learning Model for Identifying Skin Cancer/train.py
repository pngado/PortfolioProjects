from datetime import datetime
import numpy as np
import torch
import torch.nn as nn
import tqdm.notebook as tq
import wandb
import torchmetrics
from torch.utils.data import DataLoader

import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

# Determine which device on import, and then use that elsewhere.
device = torch.device("cpu")
if torch.cuda.is_available():
    device = torch.device("cuda:0")
    torch.cuda.set_device(device)


def plot_confusion_matrix(cm, class_names):
    '''
        cm: the confusion matrix that we wish to plot
        class_names: the names of the classes 
    '''

    # this normalizes the confusion matrix
    cm = cm.astype(np.float32) / cm.sum(axis=1)[:, None]
    
    df_cm = pd.DataFrame(cm, class_names, class_names)
    ax = sn.heatmap(df_cm, annot=True, cmap='flare')

    ax.set_xlabel('Predicted')
    ax.set_ylabel('True')
    plt.show()
    
def count_classes(preds):
    '''
    Counts the number of predictions per class given preds, a tensor
    shaped [batch, n_classes], where the maximum per preds[i]
    is considered the "predicted class" for batch element i.
    '''
    pred_classes = preds.argmax(dim=1)
    n_classes = preds.shape[1]
    return [(pred_classes == c).sum().item() for c in range(n_classes)]

def train_epoch(epoch, model, optimizer, criterion, loader, num_classes, device):
    '''
    Train the model on the entire training set precisely once (one epoch).
    '''

    model.train()

    # Initialize metrics
    epoch_loss = torchmetrics.MeanMetric().to(device)
    acc_metric = torchmetrics.Accuracy(task='multiclass', num_classes= num_classes).to(device)
    avg_recall = torchmetrics.classification.MulticlassRecall(num_classes=num_classes, average='macro').to(device)

    for i, (inputs, lbls) in enumerate(loader):
        inputs, lbls = inputs.to(device), lbls.to(device)

        # Update model weights

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, lbls)
        loss.backward()
        optimizer.step()

        # Accumulate metrics

        epoch_loss(loss)
        acc_metric(outputs, lbls)
        avg_recall(outputs, lbls)
        
    # Calculate epoch metrics, and store in a dictionary for wandb

    metrics_dict = {
      'Loss_train': epoch_loss.compute(), 
      'Accuracy_train': acc_metric.compute(), 
      'UAR_train': avg_recall.compute()
    }

    return metrics_dict

def val_epoch(epoch, model, criterion, loader, num_classes, device):
    '''
    Evaluate the model on the entire validation set.
    '''
    model.eval()
    
    # Initialize metrics

    epoch_loss = torchmetrics.MeanMetric().to(device)
    acc_metric = torchmetrics.Accuracy(task='multiclass', num_classes= num_classes).to(device)
    avg_recall = torchmetrics.classification.MulticlassRecall(num_classes=num_classes, average='macro').to(device)
    
    # initialize a confusion matrix torchmetrics object
    confmat = torchmetrics.ConfusionMatrix(task="multiclass", num_classes=num_classes).to(device)

    for inputs, lbls in loader:
        inputs, lbls = inputs.to(device), lbls.to(device)

        # Obtain validation loss 
        with torch.no_grad():
          outputs = model(inputs)
          loss = criterion(outputs, lbls)

        # Accumulate metrics

        epoch_loss(loss)
        acc_metric(outputs, lbls)
        avg_recall(outputs, lbls)
    
        # acculmate confusion matrix
        confmat(outputs, lbls) 
         
    # Calculate epoch metrics, and store in a dictionary for wandb

    metrics_dict = {
         'Loss_val': epoch_loss.compute(),
         'Accuracy_val': acc_metric.compute(),
         'UAR_val': avg_recall.compute()
    }

    # Compute the confusion matrix
    cm = confmat.compute().detach().cpu().numpy()

    return metrics_dict, cm
    


def train_model(model, train_loader, val_loader, optimizer, criterion,
                class_names, n_epochs, project_name, ident_str=None):
                
    num_classes = len(class_names)
    model.to(device)
    
    # Initialise Weights and Biases (wandb) project
    if ident_str is None:
      ident_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    exp_name = f"{model.__class__.__name__}_{ident_str}"
    run = wandb.init(project=project_name, name=exp_name)

    try:
        # Train by iterating over epochs
        for epoch in tq.tqdm(range(n_epochs), total=n_epochs, desc='Epochs'):
            train_metrics_dict = train_epoch(epoch, model, optimizer, criterion,
                    train_loader, num_classes, device)
                    
            val_metrics_dict, cm = val_epoch(epoch, model, criterion, 
                    val_loader, num_classes, device)
            wandb.log({**train_metrics_dict, **val_metrics_dict})
    finally:
        run.finish()

    # Plot confusion matrix from results of last val epoch
    plot_confusion_matrix(cm, class_names)

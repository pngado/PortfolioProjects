# Deep Learning Model for Identifying Skin Cancer

In this project, I create a deep learning model to classify images of skin lesions into one of seven classes:

1.   "MEL" = Melanoma
2.   "NV" = Melanocytic nevus
3.   "BCC" = Basal cell carcinoma
4.   "AKIEC" = Actinic keratosis
5.   "BKL" = Benign keratosis
6.   "DF" = Dermatofibroma
7.   "VASC" = Vascular lesion

## Dataset

The data for this task is a subset of: https://challenge2018.isic-archive.com/task3/

It contains ~3,800 images named like `ISIC_000000.jpg` and the following label files:

*   `/content/data/img/train.csv`
*   `/content/data/img/val.csv`
*   `/content/data/img/train_small.csv`
*   `/content/data/img/val_small.csv`

The `small` versions are the first 200 lines of each partition and are included for debugging purposes. 

## Techniques used

Including:
*  Data augmentation
*  Transfer learning
*  Weighted random sampler (to address class imbalance issue)
*  Weighted loss function (to address class imbalance issue)

## Results 
I was able to achieve an 85.5% accuracy and a 76.55% unweighted average recall (UAR).

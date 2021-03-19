
# ALL ACKNOWLEDGMENT GOES TO THE PAPER & REPOSITORY AUTHORS
# https://github.com/jfzhang95/pytorch-deeplab-xception

from torchvision import transforms
from torchvision import datasets

from .sb_dataset import *

import torch
import random
import numpy as np

from PIL import Image, ImageOps, ImageFilter

def PascalVOC2012_dataset(stage="train", use_sbd_dataset=True):
    if stage == "train":
        voc_train = datasets.VOCSegmentation('datasets/', year='2012', image_set='train', download=True,
                                        transforms=CustomCompose([
                                            CustomRandomHorizontalFlip(),
                                            CustomRandomScaleCrop(base_size=513, crop_size=513),
                                            CustomRandomGaussianBlur(),
                                            # NOTE: original repo has args parameter  
                                            # CustomRandomScaleCrop(base_size=args.base_size, crop_size=args.crop_size),
                                            CustomToTensor(),
                                            CustomNormalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                                        ]))
        if use_sbd_dataset:
            sbd_train = SB_dataset(stage)
            return torch.utils.data.ConcatDataset([voc_train, sbd_train])
        else:
            return voc_train
    else:
        return datasets.VOCSegmentation('datasets/', year='2012', image_set='val', download=True,
                                        transforms=CustomCompose([
                                            CustomFixScaleCrop(crop_size=513),
                                            CustomToTensor(),
                                            CustomNormalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                                        ]))

if __name__ == '__main__':
    from torch.utils.data import DataLoader
    import matplotlib.pyplot as plt

    voc_train = PascalVOC2012_dataset(stage='train')
    dataloader = DataLoader(voc_train, batch_size=3, shuffle=True, num_workers=0)
    print('Created loader')
    for ii, sample in enumerate(dataloader):
        img, gt = sample
        for jj in range(img.size()[0]):
            plt.figure()
            plt.subplot(211)
            plt.imshow(img[jj].numpy().transpose((1, 2, 0)))
            plt.subplot(212)
            plt.imshow(gt[jj].numpy())
        break

    plt.show(block=True)
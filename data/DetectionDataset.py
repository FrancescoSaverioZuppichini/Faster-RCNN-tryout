import pytube
import numpy as np
import cv2
import torch
from torch.utils.data import Dataset
from PIL import Image
from pathlib import Path


class YoloAnnotationsParser:

    def __call__(self, file_path):
        labels = []
        bboxs = []

        with open(file_path) as f:
            for line in f.readlines():
                line_split = line.split(' ')
                label = int(line_split[0])
                bbox = [float(b) for b in line_split[1:]]
                labels.append(label)
                bboxs.append(bbox)

        return labels, bboxs


class DetectionDataset(Dataset):
    def __init__(self, images_paths: [str], annotations_paths: [str], transform: callable = None, annotations_parser: callable = YoloAnnotationsParser()):
        self.images_paths = images_paths
        self.annotations_paths = annotations_paths
        self.annotations_parser = annotations_parser
        self.transform = transform

    def __getitem__(self, idx):
        img = Image.open(self.images_paths[idx])
        labels, boxes = self.annotations_parser(self.annotations_paths[idx])

        if self.transform is not None:
            img, boxes = self.transform(img, boxes)
        labels = torch.Tensor(labels).long()
        target = dict(boxes=boxes, labels=labels)
        return img, target



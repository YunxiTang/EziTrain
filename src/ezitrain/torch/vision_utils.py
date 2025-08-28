import torch
from PIL.Image import Image
import numpy as np


def to_pil(img: torch.Tensor):
    """convert imgage tensor to pil image"""
    img = np.moveaxis(img.numpy() * 255, 0, -1)
    return Image.fromarray(img.astype(np.uint8))

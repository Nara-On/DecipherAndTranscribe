import cv2
import numpy as np
from . import doc_augment_lib as da
import random


def augmentor(img):
    """
    Normalised input between 0.0 - 1.0
    """
    h, w = img.shape
    r = random.choice([0, 1, 2])
    salt = da.Salt(img, 0.001)
    pepper = da.Pepper(salt, 0.1)
    if r == 0:
        blur = da.LensBlur(pepper, lens_blur=(0.0, 3.0))
    elif r == 1:
        blur = da.Sharpen(pepper, lens_blur=(1.0, 3.0))
    else:
        blur = pepper
    gamma = da.GammaCorrection(blur, gamma=(0.3, 3.0))

    return gamma

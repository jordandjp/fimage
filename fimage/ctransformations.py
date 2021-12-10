"""Color transformations."""


import abc
import math
from typing import Dict

import numpy as np
from fimage.image_array import ImageArray


class CTransformation(abc.ABC):
    @abc.abstractmethod
    def process(self, image_array: ImageArray) -> None:
        pass


class Sepia(CTransformation):
    def __init__(self, adjust: int = 100) -> None:
        self.adjust = adjust / 100

    def process(self, image_array: ImageArray) -> None:
        image_array.R = (
            image_array.R * (1 - (0.607 * self.adjust))
            + (image_array.G * (0.769 * self.adjust))
            + (image_array.B * (0.189 * self.adjust))
        )
        image_array.G = (
            (image_array.R * (0.349 * self.adjust))
            + (image_array.G * (1 - (0.314 * self.adjust)))
            + (image_array.B * (0.168 * self.adjust))
        )
        image_array.B = (
            (image_array.R * (0.272 * self.adjust))
            + (image_array.G * (0.534 * self.adjust))
            + (image_array.B * (1 - (0.869 * self.adjust)))
        )
        image_array.constrain_channels()


class Contrast(CTransformation):
    def __init__(self, adjust: int = 100) -> None:
        self.adjust = math.pow((adjust + 100) / 100, 2)

    def process(self, image_array: ImageArray) -> None:
        image_array.R = image_array.R / 255
        image_array.R -= 0.5
        image_array.R *= self.adjust
        image_array.R += 0.5
        image_array.R *= 255

        image_array.G = image_array.G / 255
        image_array.G -= 0.5
        image_array.G *= self.adjust
        image_array.G += 0.5
        image_array.G *= 255

        image_array.B = image_array.B / 255
        image_array.B -= 0.5
        image_array.B *= self.adjust
        image_array.B += 0.5
        image_array.B *= 255
        image_array.constrain_channels()


class Brightness(CTransformation):
    def __init__(self, adjust: int = 0) -> None:
        self.adjust = math.floor(255 * (adjust / 100))

    def process(self, image_array: ImageArray) -> None:
        image_array.R += self.adjust
        image_array.G += self.adjust
        image_array.B += self.adjust
        image_array.constrain_channels()


class Saturation(CTransformation):
    def __init__(self, adjust: int = 0) -> None:
        self.adjust = adjust * -0.01

    def process(self, image_array: ImageArray) -> None:
        ndarray = image_array.get_current()

        max_array = ndarray.max(axis=2)
        max_array = np.repeat(max_array, 3).reshape(ndarray.shape)

        sat_array = np.where(
            max_array != ndarray, ndarray + (max_array - ndarray) * self.adjust, ndarray
        )
        image_array.R = sat_array[..., 0]
        image_array.G = sat_array[..., 1]
        image_array.B = sat_array[..., 2]
        image_array.constrain_channels()


class Invert(CTransformation):
    def process(self, image_array: ImageArray) -> None:
        image_array.R = 255 - image_array.R
        image_array.G = 255 - image_array.G
        image_array.B = 255 - image_array.B
        image_array.constrain_channels()


class Gamma(CTransformation):
    def __init__(self, adjust: int = 1) -> None:
        self.adjust = adjust

    def process(self, image_array: ImageArray) -> None:
        f = np.vectorize(self.f)
        image_array.R = ((image_array.R / 255) ** self.adjust) * 255
        image_array.G = ((image_array.G / 255) ** self.adjust) * 255
        image_array.B = ((image_array.B / 255) ** self.adjust) * 255
        image_array.constrain_channels()


class Noise(CTransformation):
    def __init__(self, adjust: int = 1) -> None:
        self.adjust = abs(adjust) * 2.55
    
    def process(self, image_array: ImageArray) -> None:
        # Generate a random array and sum it up with our current one
        random_array = np.random.randint(-self.adjust, self.adjust, image_array.original_array.shape)
        ndarray = image_array.get_current()
        ndarray = ndarray + random_array

        image_array.R = ndarray[..., 0]
        image_array.G = ndarray[..., 1]
        image_array.B = ndarray[..., 2]

        image_array.constrain_channels()


class Clip(CTransformation):
    def __init__(self, adjust: int = 1) -> None:
        self.adjust = abs(adjust) * 2.55

    def process(self, image_array: ImageArray) -> None:
        ndarray = image_array.get_current()

        ndarray = np.where(ndarray > 255 - self.adjust, 255, ndarray)
        ndarray = np.where(ndarray < self.adjust, 0, ndarray)

        image_array.R = ndarray[..., 0]
        image_array.G = ndarray[..., 1]
        image_array.B = ndarray[..., 2]


class Channels(CTransformation):
    def __init__(self, channels: Dict = dict) -> None:
        self.R = channels.get('R')
        self.G = channels.get('G')
        self.B  = channels.get('B')

        if self.R:
            self.R /= 100 
        
        if self.G:
            self.G /= 100 

        if self.B:
            self.B /= 100 

    def process(self, image_array: ImageArray) -> None:
        if self.R is not None:
            if self.R > 0:
                image_array.R = image_array.R + (255 - image_array.R) * self.R
            else:
                image_array.R = image_array.R + (255 - image_array.R) * abs(self.R)
        
        if self.G is not None:
            if self.G > 0:
                image_array.G = image_array.G + (255 - image_array.G) * self.G
            else:
                image_array.G = image_array.G + (255 - image_array.G) * abs(self.G)

        if self.B is not None:
            if self.B > 0:
                image_array.B = image_array.B + (255 - image_array.B) * self.B
            else:
                image_array.B = image_array.B + (255 - image_array.B) * abs(self.B)

        image_array.constrain_channels()
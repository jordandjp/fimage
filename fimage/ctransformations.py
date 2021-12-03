"""Color transformations."""


import abc
import math

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

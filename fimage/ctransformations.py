"""Color transformations."""


import abc
import math

import numpy as np

from fimage.image_array import ImageArray
from fimage.converters import rgb2hsv, hsv2rgb


class CTransformation(abc.ABC):
    @abc.abstractmethod
    def process(self, image_array: ImageArray) -> None:
        pass


class FillColor(CTransformation):
    def __init__(self, R, G, B) -> None:
        self.R = R
        self.G = G
        self.B = B

    def process(self, image_array: ImageArray) -> None:
        image_array.R = self.R
        image_array.G = self.G
        image_array.B = self.B


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
        axis = ndarray.ndim - 1

        max_array = ndarray.max(axis=axis)
        max_array = np.repeat(max_array, 3).reshape(ndarray.shape)

        sat_array = np.where(
            ndarray != max_array, ndarray + (max_array - ndarray) * self.adjust, ndarray
        )
        image_array.R = sat_array[..., 0]
        image_array.G = sat_array[..., 1]
        image_array.B = sat_array[..., 2]
        image_array.constrain_channels()


class Vibrance(CTransformation):
    def __init__(self, adjust: int = 0) -> None:
        self.adjust = adjust * -1

    def process(self, image_array: ImageArray) -> None:
        ndarray = image_array.get_current()
        axis = ndarray.ndim - 1

        max_array = ndarray.max(axis=axis)
        max_array = np.repeat(max_array, 3).reshape(ndarray.shape)

        avg_array = np.mean(ndarray, axis=axis, dtype=np.uint8)
        avg_array = np.repeat(avg_array, 3).reshape(ndarray.shape)

        amt_array = (((max_array - avg_array) * 2 / 255) * self.adjust) / 100

        vib_array = np.where(
            ndarray != max_array, ndarray + (max_array - ndarray) * amt_array, ndarray
        )
        image_array.R = vib_array[..., 0]
        image_array.G = vib_array[..., 1]
        image_array.B = vib_array[..., 2]
        image_array.constrain_channels()


class Greyscale(CTransformation):
    def process(self, image_array: ImageArray) -> None:
        avg = (
            (0.299 * image_array.R) + (0.587 * image_array.G) + (0.114 * image_array.B)
        )
        image_array.R = avg
        image_array.G = avg
        image_array.B = avg


class Hue(CTransformation):
    def __init__(self, adjust) -> None:
        self.adjust = abs(adjust)

    def process(self, image_array: ImageArray) -> None:
        hsv = rgb2hsv(image_array.get_current())
        h = hsv[..., 0]
        h *= 100
        h += self.adjust
        h = h % 100
        h = h / 100
        hsv[..., 0] = h
        # hsv2rgb function returns a float type with values ranging from 0 to 1
        rgb = (hsv2rgb(hsv) * 255).astype(np.uint8)
        image_array.R = rgb[..., 0]
        image_array.G = rgb[..., 1]
        image_array.B = rgb[..., 2]
        image_array.constrain_channels()


class Colorize(CTransformation):
    def __init__(self, R, G, B, level) -> None:
        self.R = R
        self.G = G
        self.B = B
        self.level = level

    def process(self, image_array: ImageArray) -> None:
        image_array.R = image_array.R - (image_array.R - self.R) * (self.level / 100)
        image_array.G = image_array.G - (image_array.G - self.G) * (self.level / 100)
        image_array.B = image_array.B - (image_array.B - self.B) * (self.level / 100)
        image_array.constrain_channels()

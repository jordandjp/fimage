"""Color transformations."""


import abc
import math
from typing import Dict, Tuple

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
        ndarray = image_array.get_current().astype(np.int16)
        ndarray += self.adjust
        image_array.R = ndarray[..., 0]
        image_array.G = ndarray[..., 1]
        image_array.B = ndarray[..., 2]
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
        image_array.R = ((image_array.R / 255) ** self.adjust) * 255
        image_array.G = ((image_array.G / 255) ** self.adjust) * 255
        image_array.B = ((image_array.B / 255) ** self.adjust) * 255
        image_array.constrain_channels()


class Noise(CTransformation):
    def __init__(self, adjust: int = 1) -> None:
        self.adjust = abs(adjust) * 2.55

    def process(self, image_array: ImageArray) -> None:
        # Generate a random array and sum it up with our current one
        random_array = np.random.randint(
            -self.adjust, self.adjust, image_array.original_array.shape
        )
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
        self.R = channels.get("R")
        self.G = channels.get("G")
        self.B = channels.get("B")

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


class Curves(CTransformation):
    def __init__(self, p0: Tuple, p1: Tuple, p2: Tuple, p3: Tuple) -> None:
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.curve = self.calculate_bezier(1000)

    def clip(self, x: int) -> int:
        if x < 0:
            return 0

        if x > 255:
            return 255

        return x

    def missing_values(self, curve: Dict) -> Dict:
        max_value = 256

        if len(curve.keys()) < max_value:
            # Some values might be missed, we need to add them
            right_value = None
            left_value = None

            for index in range(max_value):
                if index not in curve.keys():
                    left_value = curve.get(index - 1)
                    for i in range(index, max_value):
                        if i in curve.keys():
                            right_value = curve.get(i)
                            break

                    if left_value is not None and right_value is not None:
                        curve[index] = round((left_value + right_value) / 2)

                    if left_value is None:
                        curve[index] = right_value

                    if right_value is None:
                        curve[index] = left_value

        return curve

    def calculate_bezier(self, granuality: int) -> Dict:
        result = dict()

        for i in range(granuality):
            t = i / granuality
            x = (
                (1 - t) ** 3 * self.p0[0]
                + 3 * (1 - t) ** 2 * t * self.p1[0]
                + 3 * (1 - t) * t ** 2 * self.p2[0]
                + t ** 3 * self.p3[0]
            )
            y = (
                (1 - t) ** 3 * self.p0[1]
                + 3 * (1 - t) ** 2 * t * self.p1[1]
                + 3 * (1 - t) * t ** 2 * self.p2[1]
                + t ** 3 * self.p3[1]
            )

            result[round(x)] = round(self.clip(y))

        result = self.missing_values(result)

        return result

    def process(self, image_array: ImageArray) -> None:
        # https://stackoverflow.com/a/16993364
        ndarray = image_array.get_current()

        u, inv = np.unique(ndarray, return_inverse=True)
        ndarray = np.array([self.curve.get(x) for x in u])[inv].reshape(ndarray.shape)

        image_array.R = ndarray[..., 0]
        image_array.G = ndarray[..., 1]
        image_array.B = ndarray[..., 2]


class Exposure(CTransformation):
    def __init__(self, adjust: int = 1) -> None:
        self.adjust = abs(adjust) / 100
        self.p1 = (0, self.adjust * 255)
        self.p2 = (255 - (self.adjust * 255), 255)

    def process(self, image_array: ImageArray) -> None:
        Curves((0, 0), self.p1, self.p2, (255, 255)).process(image_array)

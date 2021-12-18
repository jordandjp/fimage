"""Filters."""


from fimage.ctransformations import (
    Brightness,
    Clip,
    Colorize,
    Contrast,
    Curves,
    Exposure,
    Gamma,
    Grayscale,
    Posterize,
    Saturation,
    Vibrance,
)
from fimage.image_array import ImageArray


class Filter:
    @classmethod
    def process(cls, image_array: ImageArray) -> None:
        for transformation in cls.transformations:
            transformation.process(image_array)


class Love(Filter):
    transformations = [
        Brightness(5),
        Exposure(8),
        Contrast(4),
        Colorize(196, 32, 7, 30),
        Vibrance(50),
        Gamma(1.3),
    ]


class OrangePeel(Filter):
    transformations = [
        Curves((0, 0), (100, 50), (140, 200), (255, 255)),
        Vibrance(-30),
        Saturation(-30),
        Colorize(255, 144, 0, 30),
        Contrast(-5),
        Gamma(1.4),
    ]


class sinCity(Filter):
    transformations = [
        Contrast(100),
        Vibrance(15),
        Exposure(10),
        Posterize(80),
        Clip(30),
        Grayscale(),
    ]

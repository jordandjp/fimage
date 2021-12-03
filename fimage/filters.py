"""Filters."""


from fimage.image_array import ImageArray
from fimage.ctransformations import Sepia, Contrast


class Filter:
    @classmethod
    def process(cls, image_array: ImageArray) -> None:
        for transformation in cls.transformations:
            transformation.process(image_array)

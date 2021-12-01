"""Filters."""


from fimage.channels import Channels
from fimage.ctransformations import Sepia, Contrast


class Filter:
    @classmethod
    def process(cls, channels: Channels) -> None:
        for transformation in cls.transformations:
            transformation.process(channels)


class ContrastSepia(Filter):
    transformations = [Contrast(50), Sepia(100)]

"""Color transformations."""


import abc
import math

from fimage.channels import Channels


class CTransformation(abc.ABC):
    @abc.abstractmethod
    def process(self, channels: Channels) -> None:
        pass


class Sepia(CTransformation):
    def __init__(self, adjust: int = 100) -> None:
        self.adjust = adjust / 100

    def process(self, channels: Channels) -> None:
        channels.R = (
            channels.R * (1 - (0.607 * self.adjust))
            + (channels.G * (0.769 * self.adjust))
            + (channels.B * (0.189 * self.adjust))
        )
        channels.G = (
            (channels.R * (0.349 * self.adjust))
            + (channels.G * (1 - (0.314 * self.adjust)))
            + (channels.B * (0.168 * self.adjust))
        )
        channels.B = (
            (channels.R * (0.272 * self.adjust))
            + (channels.G * (0.534 * self.adjust))
            + (channels.B * (1 - (0.869 * self.adjust)))
        )
        channels.constrain_channels()


class Contrast(CTransformation):
    def __init__(self, adjust: int = 100) -> None:
        self.adjust = math.pow((adjust + 100) / 100, 2)

    def process(self, channels: Channels) -> None:
        channels.R = channels.R / 255
        channels.R -= 0.5
        channels.R *= self.adjust
        channels.R += 0.5
        channels.R *= 255

        channels.G = channels.G / 255
        channels.G -= 0.5
        channels.G *= self.adjust
        channels.G += 0.5
        channels.G *= 255

        channels.B = channels.B / 255
        channels.B -= 0.5
        channels.B *= self.adjust
        channels.B += 0.5
        channels.B *= 255
        channels.constrain_channels()

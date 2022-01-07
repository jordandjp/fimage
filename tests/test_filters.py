import numpy as np
import pytest

from fimage.filters import Brightness, FillColor, Grayscale, Hue, Saturation, Sepia
from fimage.image_array import ImageArray


@pytest.fixture
def initial_image_array():
    return ImageArray(
        np.array(
            [
                [[246, 180, 255], [5, 17, 12]],
                [[45, 70, 70], [145, 135, 10]],
            ]
        )
    )


def test_fill_color(initial_image_array):
    FillColor(10, 20, 30).process(initial_image_array)
    desire_array = np.array(
        [
            [[10, 20, 30], [10, 20, 30]],
            [[10, 20, 30], [10, 20, 30]],
        ]
    )
    np.testing.assert_equal(initial_image_array.get_current(), desire_array)


def test_brightness(initial_image_array):
    Brightness(20).process(initial_image_array)
    desire_array = np.array(
        [
            [[255, 231, 255], [56, 68, 63]],
            [[96, 121, 121], [196, 186, 61]],
        ]
    )
    np.testing.assert_equal(initial_image_array.get_current(), desire_array)


def test_saturation(initial_image_array):
    Saturation(10).process(initial_image_array)
    desire_array = np.array(
        [
            [[245, 172, 255], [3, 17, 11]],
            [[42, 70, 70], [145, 134, 0]],
        ]
    )
    np.testing.assert_equal(initial_image_array.get_current(), desire_array)


def test_grayscale(initial_image_array):
    Grayscale().process(initial_image_array)
    desire_array = [
        [[208, 208, 208], [12, 12, 12]],
        [[62, 62, 62], [123, 123, 123]],
    ]
    np.testing.assert_equal(initial_image_array.get_current(), desire_array)


def test_sepia(initial_image_array):
    Sepia(50).process(initial_image_array)
    desire_array = [
        [[255, 219, 238], [11, 17, 12]],
        [[64, 76, 68], [153, 141, 64]],
    ]
    np.testing.assert_equal(initial_image_array.get_current(), desire_array)


def test_hue(initial_image_array):
    Hue(50).process(initial_image_array)
    desire_array = [
        [[189, 255, 180], [17, 5, 10]],
        [[70, 45, 45], [10, 19, 145]],
    ]
    np.testing.assert_allclose(
        initial_image_array.get_current(), desire_array, atol=1.0
    )

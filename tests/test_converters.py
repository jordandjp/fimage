import numpy as np
import pytest

from fimage.converters import hsv2rgb, rgb2hsv


@pytest.fixture
def initial_rgb_array():
    return np.array(
        [
            [[246, 180, 255], [5, 17, 12]],
            [[45, 70, 70], [145, 135, 10]],
            [[0, 0, 0], [255, 255, 255]],
            [[10, 255, 5], [252, 3, 255]],
        ]
    )


@pytest.fixture
def initial_hsv_array():
    return np.array(
        [
            [[163 / 360, 5 / 100, 100 / 100], [194 / 360, 35 / 100, 27 / 100]],
            [[285 / 360, 4 / 100, 73 / 100], [140 / 360, 30 / 100, 17 / 100]],
            [[0 / 360, 4 / 100, 6 / 100], [300 / 360, 0 / 100, 0 / 100]],
            [[0 / 360, 100 / 100, 1 / 100], [0 / 360, 95 / 100, 95 / 100]],
        ]
    )


def test_rgb2hsv(initial_rgb_array):
    hsv_array = rgb2hsv(initial_rgb_array)
    desired_array = np.array(
        [
            [[293 / 360, 29.4 / 100, 100 / 100], [155 / 360, 70.6 / 100, 6.7 / 100]],
            [[180 / 360, 35.7 / 100, 27.5 / 100], [56 / 360, 93.1 / 100, 56.9 / 100]],
            [[0 / 360, 0 / 100, 0 / 100], [0 / 360, 0 / 100, 100 / 100]],
            [[119 / 360, 98 / 100, 100 / 100], [300 / 360, 98.9 / 100, 100 / 100]],
        ]
    )
    np.testing.assert_allclose(hsv_array, desired_array, atol=0.5)


def test_hsv2rgb(initial_hsv_array):
    rgb_array = hsv2rgb(initial_hsv_array)
    desired_array = np.array(
        [
            [[242 / 255, 255 / 255, 251 / 255], [45 / 255, 63 / 255, 69 / 255]],
            [[184 / 255, 179 / 255, 186 / 255], [30 / 255, 43 / 255, 35 / 255]],
            [[15 / 255, 15 / 255, 15 / 255], [0 / 255, 0 / 255, 0 / 255]],
            [[2 / 255, 0 / 255, 0 / 255], [242 / 255, 12 / 255, 12 / 255]],
        ]
    )
    np.testing.assert_allclose(rgb_array, desired_array, atol=0.5)

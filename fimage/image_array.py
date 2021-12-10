import numpy as np


class ImageArray:
    def __init__(self, ndarray: np.ndarray) -> None:
        self.original_array = ndarray
        self.R = self.original_array[..., 0]
        self.G = self.original_array[..., 1]
        self.B = self.original_array[..., 2]

    def constrain_channels(self) -> None:
        new_array = np.array([self.R, self.G, self.B], dtype=np.int16)
        np.clip(new_array, 0, 255, out=new_array)
        self.R, self.G, self.B = new_array

    def get_current(self) -> np.ndarray:
        """Return an array with the original shape and updated RGB values."""
        new_array = np.empty(self.original_array.shape, dtype=np.uint8)
        new_array[..., 0] = self.R
        new_array[..., 1] = self.G
        new_array[..., 2] = self.B
        return new_array

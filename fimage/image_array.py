import numpy as np


class ImageArray:
    def __init__(self, ndarray: np.ndarray) -> None:
        self.shape = ndarray.shape
        self.R = ndarray[..., 0]
        self.G = ndarray[..., 1]
        self.B = ndarray[..., 2]
        self.A = None

        if self.shape[-1] == 4:
            self.A = ndarray[..., 3]

    @property
    def has_alpha(self):
        return True if self.A is not None else False

    def constrain_channels(self) -> None:
        new_array = np.array([self.R, self.G, self.B], dtype=np.int16)
        np.clip(new_array, 0, 255, out=new_array)
        self.R, self.G, self.B = new_array

    def get_current(self) -> np.ndarray:
        """Return an array with the original shape and updated RGB(A) values."""
        new_array = np.empty(self.shape, dtype=np.uint8)
        new_array[..., 0] = self.R
        new_array[..., 1] = self.G
        new_array[..., 2] = self.B
        if self.has_alpha:
            new_array[..., 3] = self.A
        return new_array

    def get_current_rgb(self) -> np.ndarray:
        """Return an array with only RGB values."""
        rgb_shape = self.shape[:-1] + (3,)
        new_array = np.empty(rgb_shape, dtype=np.uint8)
        new_array[..., 0] = self.R
        new_array[..., 1] = self.G
        new_array[..., 2] = self.B
        return new_array

import numpy as np


class Channels:
    def __init__(self, R: np.ndarray, G: np.ndarray, B: np.ndarray) -> None:
        self.R = R
        self.G = G
        self.B = B

    def constrain_channels(self) -> None:
        new_array = np.array([self.R, self.G, self.B], dtype=np.int16)
        np.clip(new_array, 0, 255, out=new_array)
        self.R, self.G, self.B = new_array

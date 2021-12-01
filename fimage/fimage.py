from PIL import Image
import numpy as np

from fimage.channels import Channels


class FImage:
    def __init__(self, img) -> None:
        self.img = Image.open(img)
        self.img_array = np.array(self.img)

        self.channels = Channels(
            self.img_array[:, :, 0],  # R
            self.img_array[:, :, 1],  # G
            self.img_array[:, :, 2],  # B
        )

    def apply(self, *filters):
        for t in filters:
            t.process(self.channels)

        return self.ndarray_to_img()

    def ndarray_to_img(self):
        new_array = np.empty(self.img_array.shape, dtype=np.int8)
        new_array[:, :, 0] = self.channels.R
        new_array[:, :, 1] = self.channels.G
        new_array[:, :, 2] = self.channels.B

        return Image.fromarray(new_array, "RGB")

    def save(self, *args, **kwargs):
        self.img.save(*args, **kwargs)

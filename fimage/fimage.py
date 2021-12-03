from PIL import Image
import numpy as np

from fimage.image_array import ImageArray


class FImage:
    def __init__(self, img) -> None:
        self.img = Image.open(img)
        self.image_array = ImageArray(np.array(self.img))

    def apply(self, *filters):
        for t in filters:
            t.process(self.image_array)

        return self.ndarray_to_img()

    def ndarray_to_img(self):
        return Image.fromarray(self.image_array.get_current(), "RGB")

    def save(self, *args, **kwargs):
        self.img.save(*args, **kwargs)

import numpy as np
from PIL import Image

from fimage.image_array import ImageArray


class FImage:
    def __init__(self, image) -> None:
        self.original_image = Image.open(image)
        self.image = self.original_image
        self.exif_data = self.image.getexif()
        self.image_array = ImageArray(np.array(self.image))

    def apply(self, *filters):
        for t in filters:
            t.process(self.image_array)

        self.image = self.ndarray_to_image()

    def ndarray_to_image(self):
        return Image.fromarray(self.image_array.get_current(), "RGB")

    def save(self, *args, **kwargs):
        self.image.save(exif=self.exif_data, *args, **kwargs)

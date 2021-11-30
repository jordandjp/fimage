import abc
import math

from PIL import Image
import numpy as np


class Transformation(abc.ABC):
    @abc.abstractmethod
    def process(self, ndarray):
        pass

class Sepia(Transformation):
    def __init__(self, adjust = 100) -> None:
        self.adjust = adjust / 100

    def process(self, R, G, B) -> np.array:
        R = (R * (1 - (0.607 * self.adjust)) + (G * (0.769 * self.adjust)) + (B * (0.189 * self.adjust)))
        G = (R * (0.349 * self.adjust)) + (G * (1 - (0.314 * self.adjust))) + (B * (0.168 * self.adjust))
        B = (R * (0.272 * self.adjust)) + (G * (0.534 * self.adjust)) + (B * (1 - (0.869 * self.adjust)))
        
        return R, G, B


class Contrast(Transformation):
    def __init__(self, adjust = 100) -> None:
        self.adjust = math.pow((adjust + 100) / 100, 2)
    
    def process(self, R, G, B) -> np.array:
        R = R / 255
        R -= 0.5
        R *= self.adjust
        R += 0.5
        R *= 255
        
        G = G / 255
        G -= 0.5
        G *= self.adjust
        G += 0.5
        G *= 255

        B = B / 255
        B -= 0.5
        B *= self.adjust
        B += 0.5
        B *= 255
        
        return R, G, B

    
class FImage():
    def __init__(self, img) -> None:
        self.img = Image.open(img)
        self.img_array = np.array(self.img)
        self.transformations = [Contrast(50), Sepia(100)]
    
    def apply(self):
        R, G, B = self.img_array[:, :, 0], self.img_array[:, :, 1], self.img_array[:, :, 2]
        for t in self.transformations:
            R, G, B = t.process(R, G, B)
            R, G, B = constrain_RGB(self.img_array, R, G, B)
            
        new_array = np.empty(self.img_array.shape, dtype=np.int8)
        new_array[:, :, 0] = R
        new_array[:, :, 1] = G
        new_array[:, :, 2] = B
               
        return Image.fromarray(new_array, 'RGB')
        
    def save(self, *args, **kwargs):
        self.img.save(*args, **kwargs)


def constrain_RGB(ndarray, R, G, B):
    new_array = np.empty(ndarray.shape, dtype=np.int16)
    new_array[:, :, 0] = R
    new_array[:, :, 1] = G
    new_array[:, :, 2] = B
    np.clip(new_array, 0, 255, out=new_array)
    R, G, B = new_array[:, :, 0], new_array[:, :, 1], new_array[:, :, 2]
    return R, G, B

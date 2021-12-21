# FImage

A Python module to apply and create multiples filters to images.

You need to be using Python 3.6 or greater to be able to use **FImage**.

## Installation
```python
pip install fimage
```

## Example

### A Simple filter

Create a file `app.py`  with:

```python
from fimage import FImage
from fimage.filters import Sepia


def main():
    # replace 'my_picture.jpg' with the path to your image
    image = FImage('my_picture.jpg')

    # apply the Sepia filter to the image
    image.apply(Sepia(90))

    # save the image with the applied filter
    image.save('my_picture_sepia.jpg')


if __name__ == "__main__":
    main()
```

Now, just run it :

```python
python app.py
```

This is `my_picture.jpg` before the filter was applied

<img alt="my_picture.jpg" src="examples/img/my_picture.jpg" width="400" height="500">

And this is how new image `my_picture_sepia.jpg` looks like after the filter was applied

<img alt="my_picture_sepia.jpg" src="examples/img/my_picture_sepia.jpg" width="400" height="500">

**Note**:  *90 represents the adjustment value we want to use for applying a sepia tone to this picture, lower values will result an image with less sepia tone while higher values will give us an image with a notorious sepia tone.*

Most of the filters **FImage** offers will need an adjustment value to be passed.

### Applying multiple filters

**FImage** offers more filters besides the Sepia one, even you can combine multiples filters to give a better look to your picture.

Modify the file `app.py` to import more filters from **FImage**

```python
from fimage import FImage
from fimage.filters import Contrast, Brightness, Saturation


def main():
    image = FImage('my_picture.jpg')

    # apply the mutiple filters to the image
    image.apply(
        Saturation(20),
        Contrast(25),
        Brightness(15)
    )

    # save the image with the applied filter
    image.save('my_picture_mixed.jpg')


if __name__ == "__main__":
    main()
```

We run it by

```python
python app.py
```

And our new `my_picture_mixed.jpg` looks like

<img alt="my_picture_mixed.jpg" src="examples/img/my_picture_mixed.jpg" width="400" height="500">

The order in which the filters are passed to the `apply` function matters, this is because the filters are applied in a sequential manner, so the next filter will be applied over the resultant image from the previous one.

Currently **FImage** supports the following filters:
- **FillColor**
- **Sepia**
- **Contrast**
- **Brightness**
- **Saturation**
- **Vibrance**
- **Grayscale**
- **Hue**
- **Colorize**
- **Invert**
- **Gamma**
- **Noise**
- **Clip**
- **Exposure**

### Presets

Presets are just the combinations of multiple filters with already defined adjustment values.

Let’s change our `app.py` one more time to use the Presets
```python
from fimage import FImage
from fimage.presets import SinCity


def main():
    # replace 'my_picture.jpg' with the path to your image
    image = FImage('my_picture.jpg')

    # apply the SinCity preset to the image
    image.apply(SinCity())

    # save the image with the applied preset
    image.save('my_picture_sincity.jpg')


if __name__ == "__main__":
    main()
```

 After we run it, we get our new  `my_picture_sincity.jpg`

<img alt="my_picture_sincity.jpg" src="examples/img/my_picture_sincity.jpg" width="400" height="500">

Currently supported Presets:
- **SinCity**
- **OrangePeel**
- **Love**

### Custom Presets
If you like the look your picture got after testing different filters and want to store this combination for applying it to more pictures, you can create your own Preset by just extending the `Preset` Class and specifying these filters and their adjust values in it.

In our `app.py` let’s do

```python
from fimage import FImage
from fimage.presets import Preset
from fimage.filters import Contrast, Brightness, Saturation


# Create my custom preset and specify the filters to apply
class MyOwnPreset(Preset):
    transformations = [
        Contrast(30),
        Saturation(50),
        Brightness(10),
    ]


def main():
    # replace 'my_picture.jpg' with the path to your image
    image = FImage('my_picture.jpg')

    # apply MyOwnPreset to the image
    image.apply(MyOwnPreset())

    # save the image with the applied preset
    image.save('my_picture_custom.jpg')


if __name__ == "__main__":
    main()
```

The new `my_picture_custom.jpg`

<img alt="my_picture_custom.jpg" src="examples/img/my_picture_custom.jpg" width="400" height="500">

Now, in this way `MyOwnPreset` has the combination of filters you like and you can use to modify more pictures.
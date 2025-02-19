from PIL import ImagePalette, Image
import random
from typing import Any


def generate_palette(
        size: int,
        red_amount: float = 1.0,
        green_amount: float = 1.0,
        blue_amount: float = 1.0,
        floor: int = 0,
        ceiling: int = 255
) -> ImagePalette:

    palette = []

    for i in range(0, size):
        r = random.randint(0 + floor, int(min(255 * red_amount, ceiling)))
        g = random.randint(0 + floor, int(min(255 * green_amount, ceiling)))
        b = random.randint(0 + floor, int(min(255 * blue_amount, ceiling)))

        palette.append(r)
        palette.append(g)
        palette.append(b)

    ImagePalette.ImagePalette("RGB", palette=palette)

    return palette


def shift_rgb(img: Image, pixels: Any):
    width, height = img.size

    for w in range(0, width):
        for h in range(0, height):
            r, g, b = pixels[w, h]
            pixels[w, h] = g, b, r

    return img

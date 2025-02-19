from PIL import ImagePalette
import random

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

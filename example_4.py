# started on 18th Feb 2025
from ctypes.wintypes import HPALETTE

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail@com


from PIL import Image, ImagePalette
from time import time
from math import sin, tan, tanh, cos, pi
from typing import Any

from helper_functions import generate_palette


def glitch_pixels(img: Image, pixels: Any) -> Image:
    width, height = img.size

    for w in range(0, width):
        for h in range(0, height):
            r, g, b = pixels[w, h]

            pixels[w, h] = displacement_func(r, g, b, w, h)

    return img


def average_pixel_color(pixel: tuple[int, int, int]) -> tuple[int, int, int]:
    r, g, b = pixel

    avg_value = (r + g + b) // 3

    return avg_value, avg_value, avg_value

def reduce_palette(palette_size: int, img: Any, palette):
    new_img = img.convert("P", palette=palette, colors=palette_size)

    return new_img


def displacement_func(r, g, b, h, w) -> tuple:
    new_r = int(sin(r / 255 * pi / 2)) * 255
    new_g = g
    new_b = b

    return new_r, new_g, new_b


def generate_imgs_with_random_palettes(img, num_of_imgs: int, palette_size: list[int]):
    pixels = img.load()
    width, height = img.size

    # palette = generate_palette(size=palette_size, floor=0, ceiling=185)
    palette = Image.ADAPTIVE
    for i in range(0, num_of_imgs):
        new_palette = ImagePalette.ImagePalette("RGB", palette=palette)
        image = reduce_palette(palette_size, img, new_palette)
        image.putpalette(new_palette)

        glitch_pixels(img, pixels)

        img_save_name = f"pallette-out/4/{int(time())}-{i}.png"
        image.save(img_save_name)


if __name__ == '__main__':
    image = Image.open("source-imgs/wall.jpg")

    palette_size = 12

    generate_imgs_with_random_palettes(image, 3, palette_size)


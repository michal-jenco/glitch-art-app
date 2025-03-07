# started on 18th Feb 2025
from ctypes.wintypes import HPALETTE

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image, ImagePalette
from time import time
from math import sin, tan, tanh, cos, pi
from typing import Any
from random import choice

from helper_functions import generate_palette


def glitch_pixels(img: Image.Image, i: int) -> Image:
    width, height = img.size
    pixel_image = img.convert("RGB")

    for w in range(0, width):
        for h in range(0, height):
            r, g, b = pixel_image.getpixel((w, h))

            modified_pixel = displacement_func(r, g, b, w, h, i)
            pixel_image.putpixel((w, h), modified_pixel)

    return pixel_image


def reduce_palette(palette_size: int, img: Any, palette):
    new_img = img.convert("P", palette=Image.ADAPTIVE, colors=palette_size)
    new_img = new_img.convert("P", palette=palette, colors=palette_size)
    new_img.putpalette(palette)

    return new_img


def displacement_func(r, g, b, h, w, i) -> tuple:
    # new_r = (r + ((w // 77 + 1 + i) % 74)) % 210
    # new_g = (g + h - i) % 175
    # new_b = (b + (h % 55) - w) % 200

    # new_r = (r + ((w + 1) // 5 % 40)) % (w + 1)
    # new_g = (g + h) % (h + 1)
    # new_b = (b + (h % 25) + w) // 60 % (h + 1)

    new_r = (r + ((w + 1 + i) % 54)) % 2112
    new_g = (g + h - i) % 1389
    new_b = (b + (h // 115) - w) % 105

    # new_r = int(choice((sin, tan))((b + w) / 40) * 2135)
    # new_g = int(tan((r + b + g * h) / i) / 158)
    # new_b = int(choice((tan, sin))((r * w - h) / i) / 215)

    return new_r, new_g, new_b


def generate_imgs_with_adaptive_palette(img,
                                        num_of_imgs: int,
                                        palette: ImagePalette,
                                        palette_size: int,
                                        floor: int,
                                        ceiling: int,
                                        i: int):

    for j in range(num_of_imgs):
        img = glitch_pixels(img, i)
        img = reduce_palette(palette_size, img, palette)

        img_save_name = f"pallette-out/kat/{time()}-{i}.png"
        img.save(img_save_name)



if __name__ == '__main__':
    image = Image.open("source-imgs/me/1.jpg")
    # image = Image.open("source-imgs/kat/Josef_Hrabak_1893.jpg")

    palette_size = 7
    floor = 35

    for i in range(1, 100):
        palette = generate_palette(size=palette_size)
        new_palette = ImagePalette.ImagePalette("P", palette=palette)
        image = reduce_palette(palette_size, image, new_palette)

        generate_imgs_with_adaptive_palette(image,
                                            num_of_imgs=1,
                                            palette=new_palette,
                                            palette_size=palette_size,
                                            floor = floor,
                                            ceiling = 200,
                                            i=i * 8)

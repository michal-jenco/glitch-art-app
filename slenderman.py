# started on 18th Feb 2025
from ctypes.wintypes import HPALETTE
from random import randint

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image, ImagePalette
from time import time
from typing import Any

from helper_functions import generate_palette, vary_palette


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
    new_r = (r + ((w + 1 + i) % 14)) % 2915
    new_g = (g + h - i) % 5115
    new_b = (b + (h % 55) - w) % 7210

    return new_r, new_g, new_b


def generate_imgs_with_adaptive_palette(img,
                                        palette: ImagePalette,
                                        palette_size: int,
                                        floor: int,
                                        ceiling: int,
                                        i: int):
    # Make tiny palette Image, one black pixel
    palIm = Image.new('P', (1,1))
    palIm.putpalette(palette)

    img = glitch_pixels(img, i)
    # Use "L" mode for cool CRT pixel effect
    img = img.convert("L")
    img = img.quantize(palette=palIm, dither=Image.Dither.FLOYDSTEINBERG)

    img = reduce_palette(palette_size, img, palette)

    img_save_name = f"pallette-out/slenderman/{time()}-{i}.png"
    img.save(img_save_name)


if __name__ == '__main__':
    image = Image.open("source-imgs/slenderman.jpg")

    palette_size = 7
    floor = 35

    palette = generate_palette(size=palette_size)
    palette[0], palette[1], palette[2] = 20, 5, 39
    palette[6], palette[7], palette[8] = 50, 15, 29

    for i in range(1, 128):
        palette = vary_palette(palette, 10, 10, 10, 0, 220)

        new_palette = ImagePalette.ImagePalette("P", palette=palette)
        image = reduce_palette(palette_size, image, new_palette)

        generate_imgs_with_adaptive_palette(image,
                                            palette=new_palette,
                                            palette_size=palette_size,
                                            floor = floor,
                                            ceiling = 50,
                                            i=i * 8)

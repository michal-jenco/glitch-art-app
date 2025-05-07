# started on 18th Feb 2025
from ctypes.wintypes import HPALETTE

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


# from PIL import Image, ImagePalette
# from time import time
# from math import sin, tan, tanh, cos, pi
# from typing import Any
# from random import choice
#
# from helper_functions import generate_palette
#
#
# def glitch_pixels(img: Image.Image, i: int) -> Image:
#     width, height = img.size
#     pixel_image = img.convert("RGB")
#
#     for w in range(0, width):
#         for h in range(0, height):
#             r, g, b = pixel_image.getpixel((w, h))
#
#             modified_pixel = displacement_func(r, g, b, w, h, i)
#             pixel_image.putpixel((w, h), modified_pixel)
#
#     return pixel_image
#
#
# def reduce_palette(palette_size: int, img: Any, palette):
#     new_img = img.convert("P", palette=Image.ADAPTIVE, colors=palette_size)
#     new_img = new_img.convert("P", palette=palette, colors=palette_size)
#     new_img.putpalette(palette)
#
#     return new_img
#
#
# def displacement_func(r, g, b, h, w, i) -> tuple:
#     # new_r = (r + ((w + 1 + i) % 14)) % 225
#     # new_g = (g + h - i) % 185
#     # new_b = (b + (h % 55) - w) % 240
#     #
#     # new_r = ((r + ((w % 77 + 1) % 14)) % 1777)
#     # new_g = ((g + h - i) % 2330)
#     # new_b = ((b + (h % 95) - w) % 1750)
#
#     new_r = (r + ((w + 1 + i) % 14)) % 225
#     new_g = (g + h - i) % 185
#     new_b = (b + (h % 55) - w) % 240
#
#     return new_r, new_g, new_b
#
#
# def generate_imgs_with_adaptive_palette(img,
#                                         palette: ImagePalette,
#                                         palette_size: int,
#                                         floor: int,
#                                         ceiling: int,
#                                         i: int):
#     img = glitch_pixels(img, i)
#     img = reduce_palette(palette_size, img, palette)
#
#     img_save_name = f"pallette-out/domi2/{int(time())}-{i}.png"
#     img.save(img_save_name)
#
#
# if __name__ == '__main__':
#     image = Image.open("source-imgs/domi/domi5.jpg")
#
#     palette_size = 5
#     floor = 35
#
#     for i in range(1, 33):
#         palette = generate_palette(size=palette_size)
#         new_palette = ImagePalette.ImagePalette("P", palette=palette)
#         image = reduce_palette(palette_size, image, new_palette)
#
#         generate_imgs_with_adaptive_palette(image,
#                                             palette=new_palette,
#                                             palette_size=palette_size,
#                                             floor = floor,
#                                             ceiling = 50,
#                                             i=i * 8)


# started on 18th Feb 2025

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image
from time import time
from math import  sin


def glitch_pixels(img: Image, func_r, func_g, func_b, base_wave_size: int) -> Image:
    width, height = img.size

    for w in range(0, width):
        for h in range(0, height):
            r, g, b = pixels[w, h]

            mod = int(h % 25)

            r, g, b = fractally_func_4(r, g ,b, h, w, func_r, func_g, func_b, base_wave_size, mod, mod, mod)

            pixels[w, h] = (r, g, b)

    return img

def fractally_func_4(r, g, b, h, w, f1, f2, f3,
                     base_wave_size: int,
                     wave_size_modifier_r: int = 0,
                     wave_size_modifier_g: int = 0,
                     wave_size_modifier_b: int = 0) -> tuple:
    red_amount, green_amount, blue_amount = 235, 185, 215

    new_r = f1((b + w) / (base_wave_size + wave_size_modifier_r)) * red_amount
    new_g = f2((g + h + r) / (base_wave_size + wave_size_modifier_g)) * green_amount
    new_b = f3((r + w - h) / (base_wave_size + wave_size_modifier_b)) * blue_amount

    return int(new_r), int(new_g), int(new_b)


def generate_consecutive_palettes(img: Image,
                                  image_count: int,
                                  base_wave_size: int,
                                  palette_size: int | None = None) -> Image:
    for i in range(2, image_count + 2):
        new_img = img.convert("P",
                              palette=Image.ADAPTIVE,
                              colors=i if not palette_size else palette_size
        )
        new_img = glitch_pixels(
            new_img,
            base_wave_size = base_wave_size,
            func_r = sin, func_g = sin, func_b = sin,
        )

        img_save_name = f"pallette-out/domi2/{int(time())}-{i}.png"
        img.save(img_save_name)


if __name__ == '__main__':
    image = Image.open("source-imgs/domi/domi5.jpg")

    pixels = image.load()

    generate_consecutive_palettes(image,
                                  image_count=20,
                                  palette_size=8,
                                  base_wave_size=75,
                                  )

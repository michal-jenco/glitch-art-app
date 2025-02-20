# started on 18th Feb 2025
from ctypes.wintypes import HPALETTE

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail@com


from PIL import Image, ImagePalette
from time import time
from math import sin, tan, tanh, cos, pi
from typing import Any
from random import choice

from helper_functions import generate_palette, save_image_with_cv2


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
    # new_r = (r + ((w + 1) // 5 % 40)) % (w + 1)
    # new_g = (g + h) % (h + 1)
    # new_b = (b + (h % 25) + w) // 6 % (h + 1)

    # new_r = (r + ((w + i + 1) % 114)) % 225
    # new_g = (g + h - i) % 205
    # new_b = (b + (h % 555) + w) % 240

    # new_r = int(choice((sin, tan))((b + w) / 82) * 235)
    # new_g = int(tan((r + b + g * h) / 82) * 158)
    # new_b = int(choice((tan, sin))((r * w - h) / 82) * 205)

    # new_r = (r + ((w + 1 + i) % 41)) % 225
    # new_g = (g + h - i) % 185
    # new_b = (b + (h % 55) + w) % 240

    # new_r = (r + i - ((w * i + 1) % 114)) % 225
    # new_g = (g + h + i * w) % 205
    # new_b = (b + (h % 555) + w*i) % 240

    # new_r = int(choice((sin))((b + w) / 400) * 235)
    # new_g = int(tan((r + b + g * i * h) / 500) * 158)
    # new_b = int(choice((tan))((r * w - h - i * w) / 600) * 205)

    new_r = (r + w + i) // 1 % 255
    new_g = (g + h - i) // 2 % 255
    new_b = (b + h + w + i) // 1 % 255

    return new_r, new_g, new_b


def generate_imgs_with_random_palettes(img, num_of_imgs: int, palette_size: list[int], floor: int,  ceiling: int):
    pixels = img.load()
    width, height = img.size

    for i in range(0, num_of_imgs):
        palette = generate_palette(size=palette_size, floor=floor, ceiling=ceiling)
        new_palette = ImagePalette.ImagePalette("RGB", palette=palette)
        image = reduce_palette(palette_size, img, new_palette)
        image.putpalette(new_palette)

        glitch_pixels(img, pixels)

        img_save_name = f"pallette-out/5/{int(time())}-{i}.png"
        image.save(img_save_name, compress_level=1, compress_type=3)


def generate_imgs_with_adaptive_palette(img,
                                        num_of_imgs: int,
                                        palette: ImagePalette,
                                        palette_size: int,
                                        floor: int,
                                        ceiling: int,
                                        i: int):
    img = glitch_pixels(img, i)
    img = reduce_palette(palette_size, img, palette)

    img_save_name = f"pallette-out/5/{int(time())}-{i}.png"
    img.save(img_save_name)
    # save_image_with_cv2(img=img, name=img_save_name)


if __name__ == '__main__':
    image = Image.open("source-imgs/momo1.jpg")
    img_save_name = f"pallette-out/5/{int(time())}.png"
    image.save(img_save_name)

    run_count = 16
    variant_count = 12

    for j in range(0, run_count):

        palette_size = 12
        floor = 35
        palette = generate_palette(size=palette_size, ceiling=255)
        new_palette = ImagePalette.ImagePalette("P", palette=palette)
        image = reduce_palette(palette_size, image, new_palette)

        image.save(img_save_name)

        for i in range(1, variant_count):
            print(f"run {j}/{run_count} - variant {i}/{variant_count}")
            generate_imgs_with_adaptive_palette(image,
                                                num_of_imgs=1,
                                                palette=new_palette,
                                                palette_size=palette_size,
                                                floor = floor,
                                                ceiling=200,
                                                i=i*8*2)

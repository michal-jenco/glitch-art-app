# started on 18th Feb 2025

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail@com


from PIL import Image, ImagePalette
from time import time
from math import sin, tan, tanh, cos, pi, sqrt
from typing import Any
from random import choice

from helper_functions import generate_palette


def glitch_pixels(img: Image.Image, i: int) -> Image:
    width, height = img.size
    pixel_image = img.convert("RGB")

    for w in range(0, width):
        for h in range(0, height):
            r, g, b = pixel_image.getpixel((w, h))

            modified_pixel = displacement_func(r, g, b, w, h, i, img.size)
            pixel_image.putpixel((w, h), modified_pixel)

    return pixel_image


def reduce_palette(palette_size: int, img: Any, palette):
    new_img = img.convert("P", palette=Image.ADAPTIVE, colors=palette_size)
    new_img = new_img.convert("P", palette=palette, colors=palette_size)
    new_img.putpalette(palette)

    return new_img


def displacement_func(r, g, b, h, w, i, img_size) -> tuple:
    width, height = img_size

    # new_r = (r + w + i) // 4 % 255
    # new_g = (g + h - i) // 4 % 255
    # new_b = (b + h + w + sqrt(i)) // 4 % 255

    new_r = (r + w + i) / 2 % 255
    new_g = (g + h - i) / 3 % 255
    new_b = (b + h + w + sqrt(i)) / 2 % 255

    # new_r = (r + ((w + i + 1) % 114)) % 225
    # new_g = (g + h - i) % 205
    # new_b = (b + (h % 555) + w) % 240

    # new_r = (r + ((w + i + 1) % 40)) % 225
    # new_g = ((g + h - i) % 25) % 205
    # new_b = (b + (h - i % 50) + w) % 240

    # new_r = int(choice((sin, tan))((b + w) / 82) * 235)
    # new_g = int(tan((r + b + g * h) / 82) * 158)
    # new_b = int(choice((tan, sin))((r * w - h) / 82) * 205)

    # new_r = (r + ((w + 1 + i) % 41)) % 225
    # new_g = (g + h - i) % 185
    # new_b = (b + (h % 55) + w) % 240

    # new_r = (r + i - ((w * i + 1) % 114)) % 225
    # new_g = (g + h + i * w) % 205
    # new_b = (b + (h % 555) + w*i) % 240

    # new_r = (r + ((w + 1) // 5 % 40)) % (w + 1)
    # new_g = (g + h) % (h + 1)
    # new_b = (b + (h % 25) + w) // 6 % (h + 1)
    #
    # new_r = (r + ((w + i + 1) % 114)) % 225
    # new_g = (g + h - i) % 205
    # new_b = (b + (h % 555) + w) % 240

    # new_r = int(choice((sin, tan))((b + w) / 82) * 235)
    # new_g = int(tan((r + b + g * h) / 82) * 158)
    # new_b = int(choice((tan, sin))((r * w - h) / 82) * 205)

    # new_r = int(choice((sin,))((b + w) / 400) * 235)
    # new_g = int(tan((r + b + g * i * h) / 500) * 158)
    # new_b = int(choice((tan,))((r * w - h - i * w) / 600) * 205)

    # new_r = (r - w + i) // 1 % 255
    # new_g = (g + h - i) // 2 % 255
    # new_b = (b - h + w - i) // 1 % 255

    # new_r = (r + (w % i)) % 255
    # new_g = (g + (h % i * 2)) % 200
    # new_b = (b + h + w) // 6 % 255
    #
    # new_r = (r + (((w // 4) ** abs(sin(i))) % i)) % 255
    # new_g = (g + ((h // 5) % i * 2)) % 200
    # new_b = (b + h // 3 + w // 7) % 255
    #
    # new_r = (r + (((w // 4) ** abs(sin(i))) % i)) % 255
    # new_g = (g + ((h // 5) % i * 2)) % 200
    # new_b = ((b + h // 3 + w // 7) ** abs(tanh(i ** 3))) % 255

    # new_r = (r + ((((w + 1) // 4) * abs(tan(i / ((w + 1) / 50)))) % i)) % 255
    # new_g = (g + ((h // 5) % i * 2)) % 200
    # new_b = ((b + h // 3 + w // 7) ** abs(tanh(i ** 3))) % 255

    # sin_r = sin(w / 16 * pi) * 64
    # new_r = (r + sin_r) % 256
    # new_g = 0
    # new_b = 50

    return int(new_r), int(new_g), int(new_b)


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


if __name__ == '__main__':
    image = Image.open("source-imgs/momo1.jpg")
    img_save_name = f"pallette-out/5/{int(time())}.png"
    image.save(img_save_name)

    run_count = 16
    variant_count = 20
    palette_size = 5
    floor = 35
    ceiling = 255

    for j in range(1, run_count):
        palette = generate_palette(size=palette_size)
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

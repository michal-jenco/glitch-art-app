# started on 18th Feb 2025

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail@com


from PIL import Image, ImagePalette
from time import time
from math import sin, tan, tanh, cos, pi, sqrt, sinh, cosh
from typing import Any
from random import choice

from helper_classes import EmptyFunction
from helper_functions import generate_palette, get_math_fname


def glitch_pixels(img: Image.Image, i: int, p1, p2, p3, f1, f2, f3) -> Image:
    width, height = img.size
    pixel_image = img.convert("RGB")

    for w in range(0, width):
        for h in range(0, height):
            r, g, b = pixel_image.getpixel((w, h))

            modified_pixel = displacement_func(r, g, b, w, h, i, img.size, p1, p2, p3, f1, f2, f3)
            pixel_image.putpixel((w, h), modified_pixel)

    return pixel_image


def reduce_palette(palette_size: int, img: Any, palette):
    new_img = img.convert("P", palette=Image.ADAPTIVE, colors=palette_size)
    new_img = new_img.convert("P", palette=palette, colors=palette_size)
    new_img.putpalette(palette)

    return new_img


def displacement_func(r, g, b, h, w, i, img_size, p1, p2, p3, f1, f2, f3) -> tuple:
    width, height = img_size

    # new_r = (r + w + i) / p1 % 255
    # new_g = (g + h - i) / p2 % 255
    # new_b = (b + h + w + sqrt(i)) / p3 % 255

    # new_r = (r + w + i) / f1(p1) / p1 % 255
    # new_g = (g + h - i) / f2(p2) / p2 % 255
    # new_b = (b + h + w + sqrt(i)) / f3(p3) / p3 % 255

    # new_r = (r + w + i) / f1(p1) / p1 % 255
    # new_g = (g + h - i) / f2(p2) / p2 % 255
    # new_b = (b + h + w + sqrt(abs(i))) / f3(p3) / p3 % 255

    # new_r = (f2(w / width * pi) + f3(h / height * pi)) + (r + w + i) / f1(p1) / p1 % 255
    # new_g = (f1(w / width * pi) + f1(h / height * pi)) + (g + h - i) / f2(p2) / p2 % 255
    # new_b = (f3(w / width * pi) + f2(h / height * pi)) + (b + h + w + sqrt(abs(i))) / f3(p3) / p3 % 255

    # new_r = ((sin(w / width * pi) * 20 + (w / width * i) + cos(h / height * pi)) + r) % 255
    # new_g = ((sin(w / width * pi) * 20 + (w / width * i) + cos(h / height * pi)) + g) % 255
    # new_b = ((sin(w / width * pi) * 20 + (w / width * i) + cos(h / height * pi)) + b) % 255

    new_r = (r + (w % 2)) % 255
    new_g = (g + h) % 200
    new_b = (b + h + w) // 6 % 255

    return int(new_r), int(new_g), int(new_b)


def generate_imgs_with_adaptive_palette(img,
                                        num_of_imgs: int,
                                        palette: ImagePalette,
                                        palette_size: int,
                                        floor: int,
                                        ceiling: int,
                                        i: int, p1, p2, p3,
                                        f1, f2, f3):
    img = glitch_pixels(img, i, p1, p2, p3, f1, f2, f3)
    img = reduce_palette(palette_size, img, palette)

    img_save_name = (f"pallette-out/6/{int(time())}-i{i}-c{palette_size}"
                     f"-{get_math_fname(f1)}-{get_math_fname(f2)}-{get_math_fname(f3)}"
                     f".png")
    img.save(img_save_name)


if __name__ == '__main__':
    image = Image.open("source-imgs/momo1.jpg")
    img_save_name = f"pallette-out/6/{int(time())}.png"

    run_count = 128
    variant_count = 20
    floor = 35
    ceiling = 255

    params = (2, 2, 2, 3, 3, 3, 4, 6, .6, .7, .8, 1, 1, 1)
    palette_sizes = (3, 3, 4, 5, 5, 6, 8, 7, 7)

    funcs = (tan, tanh, sin)

    for j in range(1, run_count):
        palette_size = choice(palette_sizes)
        palette = generate_palette(size=palette_size)
        new_palette = ImagePalette.ImagePalette("P", palette=palette)
        image = reduce_palette(palette_size, image, new_palette)

        image.save(f"pallette-out/6/{int(time())}-orig.png")

        p1 = choice(params)
        p2 = choice(params)
        p3 = choice(params)

        f1 = choice(funcs)
        f2 = choice(funcs)
        f3 = choice(funcs)

        try:
            for i in range(1, variant_count + 1):
                print(
                    f"{palette_size} colors - run {j}/{run_count} - variant {i}/{variant_count} {p1} {p2} {p3}"
                    f" {get_math_fname(f1)} {get_math_fname(f2)} {get_math_fname(f3)}"

                )

                i_mod = choice(list(range(-8, 8, 2)))

                generate_imgs_with_adaptive_palette(image,
                                                    num_of_imgs=1,
                                                    palette=new_palette,
                                                    palette_size=palette_size,
                                                    floor = floor,
                                                    ceiling=200,
                                                    i=int(i * i_mod),
                                                    p1=p1, p2=p2, p3=p3,
                                                    f1=f1, f2=f2, f3=f3,
                                                    )
        except Exception as e:
            print(f"skipping {e}")

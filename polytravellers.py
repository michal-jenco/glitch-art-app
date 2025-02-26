# started on 18th Feb 2025

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image, ImagePalette
from time import time
from math import  sin, tanh, cos, tan
import numpy as np
from numpy.random import choice

from helper_functions import generate_palette


def glitch_pixels(img: Image, func_r, func_g, func_b, base_wave_size: int, i: int) -> Image:
    width, height = img.size

    print(func_r, func_g, func_b)

    for w in range(0, width):
        for h in range(0, height):
            r, g, b = pixels[w, h]

            mod = int(h % 25)

            mod_r = int(h % 25)
            mod_g = int(h % 25)
            mod_b = int(h % 25)

            r, g, b = fractally_func_4(r, g ,b, h, w, func_r, func_g, func_b, base_wave_size, mod_r, mod_g, mod_b, i)

            pixels[w, h] = (r, g, b)

    return img


def glitch_pixels_numpy(img: Image, func_r, func_g, func_b, base_wave_size: int, i: int) -> Image:
    width, height = img.size

    pixels = np.array(img)

    for w in pixels:
        for h in range(0, width // 3):
            r, g, b = w[h * 3: h * 3 + 3]
            print(r, g, b)

            mod_r = int(h % 25)
            mod_g = int(h % 25)
            mod_b = int(h % 25)

            r, g, b = fractally_func_4(r, g ,b, h, w, func_r, func_g, func_b, base_wave_size, mod_r, mod_g, mod_b, i)

            pixels[w, h] = (r, g, b)
    img.putdata(pixels)

    return img


def fractally_func_4(r, g, b, h, w, f1, f2, f3,
                     base_wave_size: int,
                     wave_size_modifier_r: int = 0,
                     wave_size_modifier_g: int = 0,
                     wave_size_modifier_b: int = 0,
                     i: int = 0) -> tuple:
    red_amount, green_amount, blue_amount = 235, 185, 215

    ### this code is really, really sensitive to the value of base_wave_size - play around 255
    base_wave_size = 250
    new_r = r + .005 * (f1(b)/3 + h -(w * (i + 1))) / (base_wave_size + wave_size_modifier_r) * red_amount
    new_g = g + .005 * (f2(r)/3 + r) / (base_wave_size + wave_size_modifier_g) * green_amount
    new_b = b + .005 * (f3(g)/3 - h +(w / (i + 1))) / (base_wave_size + wave_size_modifier_b) * blue_amount

    return int(new_r), int(new_g), int(new_b)


def generate_consecutive_palettes(img: Image,
                                  image_count: int,
                                  base_wave_size: int,
                                  palette_size: int | None = None) -> Image:

    palette = generate_palette(size=palette_size)
    x = 0

    funcs = (cos, sin)
    func_r = choice(funcs)
    func_g = choice(funcs)
    func_b = choice(funcs)

    for i in range(2, image_count + 2):
        x += 1
        print(f"making img {x}")
        ############# SWITCH BLOCK 1 and 2 FOR COOL EFFECT ################

        ############# BLOCK 2 ################
        new_palette = ImagePalette.ImagePalette("P", palette=palette)
        new_img = img.convert("P", palette=new_palette, colors=palette_size)
        new_img.putpalette(palette)
        ############# BLOCK 2 ################

        ############# BLOCK 1 ################
        new_img = new_img.convert("P",
                                  palette=Image.ADAPTIVE,
                                  colors=i if not palette_size else palette_size
                                  )
        ############# BLOCK 1 ################

        new_img = glitch_pixels(
            new_img,
            base_wave_size = base_wave_size,
            func_r = func_r,
            func_g = func_g,
            func_b = func_b,
            i = i,
        )

        img_save_name = f"pallette-out/vektroid/polytravellers/polytravellers-{int(time())}-{i}.png"
        new_img.save(img_save_name)


if __name__ == '__main__':
    cnt = 30

    for i in range(0, cnt):
        print(f"making img {i}/{cnt}")
        image = Image.open("source-imgs/vektroid/polytravellers.jpg")

        pixels = image.load()

        generate_consecutive_palettes(image,
                                      image_count=32,
                                      palette_size=255
                                      ,
                                      base_wave_size=None,
                                      )

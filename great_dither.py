# started on 18th Feb 2025

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail@com


from PIL import Image, ImagePalette
from time import time
from math import sin, tan, tanh, cos, sqrt

from helper_functions import reduce_palette, generate_palette


def glitch_pixels(img: Image, func_r, func_g, func_b, base_wave_size: int) -> Image:
    width, height = img.size

    for w in range(0, width):
        for h in range(0, height):
            r, g, b = pixels[w, h]

            mod = int(h % 25)

            r, g, b = fractally_func_4(r, g, b, h, w, func_r, func_g, func_b, base_wave_size, mod, mod, mod)

            pixels[w, h] = (r, g, b)

    return img


def fractally_func_4(r, g, b, h, w, f1, f2, f3,
                     base_wave_size: int,
                     wave_size_modifier_r: int = 0,
                     wave_size_modifier_g: int = 0,
                     wave_size_modifier_b: int = 0) -> tuple:
    red_amount, green_amount, blue_amount = 235, 185, 215

    ### great highres dither
    new_r = f1((b + sqrt(w) / 6) / (base_wave_size + wave_size_modifier_r)) * red_amount
    new_g = f2((g + sqrt(h ** 2) / 13 + r) / (base_wave_size + wave_size_modifier_g)) * green_amount
    new_b = f3((r + w / 11 - h) / (base_wave_size + wave_size_modifier_b)) * blue_amount

    return int(new_r), int(new_g), int(new_b)


def generate_consecutive_palettes(img: Image,
                                  image_count: int,
                                  base_wave_size: int,
                                  palette_size: int | None = None) -> Image:
    palette = generate_palette(size=palette_size)
    range_start = 2
    for i in range(range_start, image_count + 2):
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
            base_wave_size=base_wave_size,
            func_r=sin, func_g=tan, func_b=tanh,
        )

        img_save_name = f"pallette-out/6/{int(time())}-{i}.png"

        if i != range_start:
            new_img.save(img_save_name)


if __name__ == '__main__':
    for i in range(0, 20):
        image = Image.open("source-imgs/momo1.jpg")

        pixels = image.load()

        generate_consecutive_palettes(image,
                                      image_count=2,
                                      palette_size=24,

                                      # higher this number, better the dither becomes
                                      base_wave_size=999,
                                      )

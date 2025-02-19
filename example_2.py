# started on 18th Feb 2025

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail@com


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

        img_save_name = f"pallette-out/3/{int(time())}-{i}.png"
        new_img.show()

def get_colors_from_image(img: Image) -> list[tuple] | None:
    items = img.convert('RGB').getcolors()
    rgb_colors = []

    for item in items:
        rgb_colors.append(item[1])

    return rgb_colors

if __name__ == '__main__':
    image = Image.open("source-imgs/man.jpg")

    pixels = image.load()

    generate_consecutive_palettes(image,
                                  image_count=2,
                                  palette_size=8,
                                  base_wave_size=75,
                                  )

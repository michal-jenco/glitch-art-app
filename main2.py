# started on 18th Feb 2025

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image
from random import choice
from time import time
from math import pow, sqrt, sin, pi, tan, tanh, cos


def modulo_pixels(img: Image) -> Image:
    width, height = img.size

    for w in range(0, width):  # for every pixel:
        for h in range(0, height):
            r, g, b = pixels[w, h]

            mod = int(h % 25)

            r, g, b = fractally_func_4(r, g ,b, h, w, sin, sin, sin, mod, mod, mod)

            pixels[w, h] = (r, g, b)

    return img

def displacement_func(r, g, b, h, w) -> tuple:
    new_r = (r + w) // 4 % 255
    new_g = (g + h) // 4 % 255
    new_b = (b + h + w) // 4 % 255

    return new_r, new_g, new_b


def fractally_func_1(r, g, b, h, w) -> tuple:
    new_r = (b * b + 1) % 255
    new_g = (r * (h * w * g) + 1) % 170
    new_b = (r * b + 1) % 230

    return new_r, new_g, new_b


def fractally_func_2(r, g, b, h, w) -> tuple:
    new_r = ((b + w)) % 255
    new_g = ((r + b + g + h)) % 255
    new_b = ((r + w - h)) % 255

    return int(new_r), int(new_g), int(new_b)


def fractally_func_3(r, g, b, h, w) -> tuple:
    new_r = sin((b + w) / 82) * 255
    new_g = tan((r + b + g * h) / 82) * 255
    new_b = tanh((r * w - h) / 82) * 255

    return int(new_r), int(new_g), int(new_b)


def fractally_func_4(r, g, b, h, w, f1, f2, f3,
                     wave_size_modifier_r: int = 0,
                     wave_size_modifier_g: int = 0,
                     wave_size_modifier_b: int = 0) -> tuple:
    wave_size = 75
    red_amount, green_amount, blue_amount = 235, 185, 215

    new_r = f1((b + w) / (wave_size + wave_size_modifier_r)) * red_amount
    new_g = f2((g + h + r) / (wave_size + wave_size_modifier_g)) * green_amount
    new_b = f3((r + w - h) / (wave_size + wave_size_modifier_b)) * blue_amount

    return int(new_r), int(new_g), int(new_b)


def modulo_pixels_2(img: Image) -> Image:
    width, height = img.size
    colors = get_colors_from_image(img)

    for w in range(1, width):
        for h in range(0, height):
            new_pixel_color = choice(colors)
            pixels[w, h] = new_pixel_color

    return img

def generate_consecutive_palettes(img: Image, count: int, palette_size: int | None = None) -> Image:
    for i in range(2, count + 2):
        new_img = img.convert("P",
                              palette=Image.ADAPTIVE,
                              colors=i if not palette_size else palette_size
        )
        new_img = modulo_pixels(new_img)

        img_save_name = f"pallette-out/3/{int(time())}-{i}.png"
        new_img.save(img_save_name)
        print(f"Saved img {img_save_name}")

def get_colors_from_image(img: Image) -> list[tuple] | None:
    items = img.convert('RGB').getcolors()
    rgb_colors = []

    if not items:
        return None

    for item in items:
        rgb_colors.append(item[1])

    return rgb_colors

if __name__ == '__main__':
    image = Image.open("source-imgs/man.jpg")

    pixels = image.load()  # create the pixel map

    generate_consecutive_palettes(image, 64, palette_size=8)

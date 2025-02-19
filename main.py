# started on 18th Feb 2025

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail@com


from PIL import Image, ImagePalette
from random import choice
from time import time


def modulo_pixels(img: Image) -> Image:
    width, height = img.size

    for w in range(0, width):  # for every pixel:
        for h in range(0, height):
            r, g, b = pixels[w, h]

            new_r = (r + (w % 2)) % 255
            new_g = (g + h) % 200
            new_b = (b + h + w) // 6 % 255

            pixels[w, h] = (new_r, new_g, new_b)

    return img

def modulo_pixels_2(img: Image) -> Image:
    width, height = img.size
    colors = get_colors_from_image(img)
    print(colors)

    for w in range(0, width):
        for h in range(0, height):
            new_pixel_color = choice(colors)
            # print(new_pixel_color)
            pixels[w, h] = new_pixel_color

    return img

def generate_consecutive_pallettes(img: Image, count: int) -> Image:
    for i in range(1, count + 1):
        new_img = img.convert("P", palette=Image.ADAPTIVE, colors=i)

        new_img = modulo_pixels(new_img)

        new_img.save(f"pallette-out/momo/{int(time())}-{i}.png")

def get_colors_from_image(img: Image) -> list[tuple] | None:
    items = img.convert('RGB').getcolors()
    rgb_colors = []

    if not items:
        return None

    for item in items:
        rgb_colors.append(item[1])

    return rgb_colors

if __name__ == '__main__':
    image = Image.open("source-imgs/clock.jpg")

    pixels = image.load()  # create the pixel map

    generate_consecutive_pallettes(image, 6)

# started on 18th Feb 2025

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image, ImagePalette
from time import time

from helper_functions import generate_palette


def modulo_pixels(img: Image) -> Image:
    width, height = img.size

    for w in range(0, width):
        for h in range(0, height):
            r, g, b = pixels[w, h]

            new_r = (r + (w // 53)) % 230
            new_g = (g + h // 77) % 177
            new_b = (b + h + w // 17) // 25 % 250

            pixels[w, h] = (new_r, new_g, new_b)

    return img


def generate_consecutive_palettes(img: Image, count: int) -> Image:
    palette_size =7
    palette = generate_palette(size=palette_size)
    new_palette = ImagePalette.ImagePalette("P", palette=palette)

    for i in range(2, count):
        new_img = img.convert("P",
                              palette=Image.ADAPTIVE,
                              colors=palette_size
                              )
        new_img = img.convert("P", palette=new_palette, colors=palette_size)
        new_img.putpalette(palette)

        new_img = modulo_pixels(new_img)

        img_save_name = f"pallette-out/there-is-no-threat/threat-{int(time())}-{i}.png"
        new_img.save(img_save_name)

def get_colors_from_image(img: Image) -> list[tuple] | None:
    items = img.convert('RGB').getcolors()
    rgb_colors = []

    for item in items:
        rgb_colors.append(item[1])

    return rgb_colors

if __name__ == '__main__':
    image = Image.open("source-imgs/there-is-no-threat/1.jpg")

    pixels = image.load()

    generate_consecutive_palettes(image, 18*4 )

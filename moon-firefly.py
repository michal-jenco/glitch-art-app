# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image, ImageFont, ImageDraw
import numpy as np
from time import time

from helper_functions import generate_palette


if __name__ == '__main__':
    photo = Image.open("source-imgs/moon.jpg")
    w, h = photo.size

    palette_size = 4
    pixelate_level = 4

    draw = ImageDraw.Draw(photo, mode="RGBA")
    draw.text(
        xy=(w // 2 - 400, h // 2),
        text="this is how I see you btw", font=ImageFont.truetype("arial", 25))

    palIm = Image.new('P', (1, 1))
    palette = generate_palette(palette_size)
    palIm.putpalette(palette)

    imgOut = photo.quantize(palette=palIm, dither=Image.Dither.FLOYDSTEINBERG)

    imgOut.save(f"pallette-out/moon-how-i-see-you/moon-{int(time())}.png")

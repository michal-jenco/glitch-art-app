# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com
from random import randrange

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from blend_modes import blending_functions
from time import time

from helper_functions import generate_palette, generate_stripes_overlay, reduce_palette


if __name__ == '__main__':
    photo = Image.open("source-imgs/muse.jpg")
    w, h = photo.size

    draw = ImageDraw.Draw(photo, mode="RGBA")




    for i in range(0, 100):
        for i in range(0, 5):
            draw.text(
                xy=(randrange(-500, w), randrange(0, h)),
                text="do you ever think about me?", font=ImageFont.truetype("arial", randrange(15, 58)))

        colors = generate_palette(8, group=True)

        np_photo = np.array(photo)
        # append alpha channel
        np_photo = np.dstack((np_photo, np.ones((np_photo.shape[0], np_photo.shape[1], 1)) * 255))
        np_photo = np_photo.astype(float)

        palIm = Image.new('P', (1, 1))
        palette = generate_palette(16)
        palIm.putpalette(palette)

        effects = generate_stripes_overlay(w, h, 20, 150, 15, colors)
        np_effect = np.array(effects)
        np_effect = np_effect.astype(float)

        imgOut = blending_functions.difference(np_photo, np_effect, 1.0)

        # Save images
        imgOut = np.uint8(imgOut)
        imgOut = Image.fromarray(imgOut)

        imgOut = reduce_palette(8, imgOut, palette)
        imgOut = imgOut.convert("L")
        imgOut = photo.resize(size=(w // 8, h // 8), resample=0)
        # and scale it up to get pixelate effect
        imgOut = photo.resize((w, h), resample=0)
        imgOut = imgOut.quantize(palette=palIm, dither=Image.Dither.RASTERIZE)

        imgOut.save(f"pallette-out/text1/text1-{time()}-{i}.png")
# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image, ImageFont, ImageDraw
from blend_modes import blending_functions
import numpy as np

from helper_functions import generate_palette, generate_stripes_overlay


def reduce_palette(palette_size: int, img, palette):
    new_img = img.convert("P", palette=Image.ADAPTIVE, colors=palette_size)
    new_img.putpalette(palette)

    return new_img


if __name__ == '__main__':
    photo = Image.open("source-imgs/moon.jpg")
    w, h = photo.size

    palette_size = 8

    draw = ImageDraw.Draw(photo, mode="RGBA")
    draw.text(
        xy=(w // 2 - 400, h // 2),
        text="this is how I see you btw", font=ImageFont.truetype("arial", 15))

    np_photo = np.array(photo)
    # append alpha channel
    np_photo = np.dstack((np_photo, np.ones((np_photo.shape[0], np_photo.shape[1], 1)) * 255))
    np_photo = np_photo.astype(float)

    palIm = Image.new('P', (1, 1))
    palette = generate_palette(palette_size)
    palIm.putpalette(palette)

    effects = generate_stripes_overlay(w, h, 20, 150, 15, palette)
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

    # imgOut.save(f"pallette-out/text1/text1-{time()}-{i}.png")
    imgOut.show()
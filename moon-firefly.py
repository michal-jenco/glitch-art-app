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

    # Save images
    imgOut = np.uint8(np_photo)
    imgOut = Image.fromarray(imgOut)

    imgOut = photo.resize(size=(w // palette_size, h // palette_size), resample=0)
    imgOut = photo.resize((w, h), resample=0)

    imgOut = imgOut.quantize(palette=palIm, dither=Image.Dither.RASTERIZE)

    imgOut.save(f"pallette-out/moon-how-i-see-you/moon-{int(time())}.png")
    # imgOut.show()
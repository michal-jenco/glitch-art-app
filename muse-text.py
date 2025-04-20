# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image, ImageDraw, ImageFont
import numpy as np
from time import time

from helper_functions import generate_palette


if __name__ == '__main__':

    palette_size = 8


    for i in range(0, 10):
        photo = Image.open("source-imgs/muse.jpg")
        w, h = photo.size
        draw = ImageDraw.Draw(photo, mode="RGBA")

        for i in range(0, 65):
            text_size = 1 + (i * 1.4) % 43
            x = 10 + i * 5
            y = 10 + i * 20

            draw.text(
                xy=(x, y),
                text="has it really been this long?",
                font=ImageFont.truetype("arial", text_size),
            )

        np_photo = np.array(photo)
        # append alpha channel
        np_photo = np.dstack((np_photo, np.ones((np_photo.shape[0], np_photo.shape[1], 1)) * 255))
        np_photo = np_photo.astype(float)

        palIm = Image.new('P', (1, 1))
        palette = generate_palette(palette_size)
        palIm.putpalette(palette)

        imgOut = photo.convert("L")
        imgOut = photo.resize(size=(w // 8, h // 8), resample=0)
        # and scale it up to get pixelate effect
        imgOut = photo.resize((w, h), resample=0)
        imgOut = imgOut.quantize(palette=palIm, dither=Image.Dither.RASTERIZE)

        imgOut.save(f"pallette-out/text1/text1-{time()}-{i}.png")
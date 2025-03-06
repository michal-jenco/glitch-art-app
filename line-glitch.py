# started on 18th Feb 2025

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image, ImagePalette
from time import time
from math import sin, tan, tanh, cos, pi
from typing import Any
from random import choice
import numpy as np



def glitch_pixels(image: np.array) -> Image:
    glitched_image = []

    for i, row in enumerate(image):
        glitched_rows = []

        for j, pixel in enumerate(row):
            r, g, b = pixel

            offset_r1 = int(sin((i + j / 20) / 40) * 59)
            offset_r2 = int(sin((i + 80) / 37) * 70)
            offset_r = offset_r1 + offset_r2

            offset_g1 = 0
            offset_g2 = 0
            offset_g = offset_g1 + offset_g2

            offset_b1 = int(sin((i - j / 2) / 40) * 80)
            offset_b2 = int(sin((i - 55 + 70) / 31) * 15)
            offset_b = offset_b1 + offset_b2

            new_r = min(max(r + offset_r, 0), 255)
            new_g = min(max(g + offset_g, 0), 255)
            new_b = min(max(b + offset_b, 0), 255)

            glitched_rows.append([new_r, new_g, new_b])
        glitched_image.append(glitched_rows)

    return np.array(glitched_image)



if __name__ == '__main__':
    image = Image.open("source-imgs/photos/man.jpg")

    np_image = np.array(image)
    np_image = np.int16(np_image)

    glitched_np_image = glitch_pixels(np_image)

    image_out = Image.fromarray(np.uint8(glitched_np_image))
    img_save_name = f"pallette-out/photos/{time()}.png"
    image_out.save(img_save_name)

    image_out.show()


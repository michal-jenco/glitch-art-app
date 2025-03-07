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



def glitch_pixels(image: np.array, sequence_offset: float = 0.0) -> Image:
    glitched_image = []

    for i, row in enumerate(image):
        glitched_rows = []

        for j, pixel in enumerate(row):
            r, g, b = pixel

            # func_arg_r1 = (i + j / 20 + sequence_offset * 7) / 40
            # func_arg_r2 = (i + 80) / 37
            # offset_r1 = int(sin(func_arg_r1) * 59)
            # offset_r2 = int(sin(func_arg_r2) * 70)
            # offset_r = offset_r1 + offset_r2

            # func_arg_r1 = (i + j / 3 + sequence_offset * 7) / 10
            # func_arg_r2 = (i / 5 + sequence_offset / 3) / 17
            # offset_r1 = int(sin(func_arg_r1) * 59)
            # offset_r2 = int(sin(func_arg_r2) * 70)
            # offset_r = offset_r1 + offset_r2

            func_arg_r1 = (i + j /20 + sequence_offset * 7) / 18
            func_arg_r2 = (j / 17 + sequence_offset ) / 15
            offset_r1 = int(cos(func_arg_r1) * 40)
            offset_r2 = int(sin(func_arg_r2) * 50)
            offset_r = offset_r1 + offset_r2

            # func_arg_r1 = (i + j / 18 + sequence_offset * 9) / 43
            # func_arg_r2 = (i + 75) / 35
            # offset_r1 = int(sin(func_arg_r1) * 59)
            # offset_r2 = int(sin(func_arg_r2) * 70)
            # offset_r = offset_r1 + offset_r2

            # func_arg_r1 = (i / 6 + j / 7 + sequence_offset * 9) / 7
            # func_arg_r2 = (i + 55 - sequence_offset * 17) / 35
            # offset_r1 = int(cos(func_arg_r1) * 59)
            # offset_r2 = int(sin(func_arg_r2) * 70)
            # offset_r = offset_r1 + offset_r2

            # func_arg_r1 = (i + j / 10 + sequence_offset * 7) / 19
            # func_arg_r2 = (-j + 55) / 87
            # offset_r1 = int(sin(func_arg_r1) * 30)
            # offset_r2 = int(cos(func_arg_r2) * 10)
            # offset_r = offset_r1 + offset_r2

            offset_g1 = 0
            offset_g2 = -20
            offset_g = offset_g1 + offset_g2

            offset_b1 = 0
            offset_b2 = 0
            offset_b = offset_b1 + offset_b2

            # func_arg_b1 = (i / 20 + j + sequence_offset * 70) / 70
            # func_arg_b2 = (j + 80) / 37
            # offset_b1 = int(sin(func_arg_b1) * 59)
            # offset_b2 = int(sin(func_arg_b2) * 70)
            # offset_b = offset_b1 + offset_b2

            new_r = min(max(r + offset_r, 0), 255)
            new_g = min(max(g + offset_g, 0), 255)
            new_b = min(max(b + offset_b, 0), 255)

            glitched_rows.append([new_r, new_g, new_b])
        glitched_image.append(glitched_rows)

    return np.array(glitched_image)



if __name__ == '__main__':
    image = Image.open("source-imgs/photos/fog7.jpg")

    np_image = np.array(image)
    np_image = np.int16(np_image)

    for frame_idx in range(256):
        glitched_np_image = glitch_pixels(np_image, frame_idx)

        image_out = Image.fromarray(np.uint8(glitched_np_image))
        img_save_name = f"pallette-out/i-will-fight-for-you/{time()}-frame{frame_idx}.jpg"
        image_out.save(img_save_name)

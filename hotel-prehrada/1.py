# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image
import numpy as np
from time import time
from math import sin
from pathlib import Path

from helper_functions import generate_palette, reduce_palette, average_rgb_pixel, vary_palette


def threshold_pixels(img_orig, img_palette, threshold: int):
    out = []

    for orig_row, palette_row in zip(img_orig, img_palette):
        row = []

        for orig_pixel, palette_pixel in zip(orig_row, palette_row):
            avg_orig = average_rgb_pixel(*orig_pixel)

            if avg_orig < threshold:
                row.append(orig_pixel)
            else:
                row.append(palette_pixel)

        out.append(row)
    return np.uint8(out)


basic_colors = [
    0, 0, 0,       # 0: black
    0, 0, 128,     # 1: dark blue
    0, 128, 0,     # 2: dark green
    0, 128, 128,   # 3: dark cyan
    128, 0, 0,     # 4: dark red
    128, 0, 128,   # 5: dark magenta
    128, 128, 0,   # 6: dark yellow
    192, 192, 192, # 7: light gray
    128, 128, 128, # 8: dark gray
    0, 0, 255,     # 9: blue
    0, 255, 0,     # 10: green
    0, 255, 255,   # 11: cyan
    255, 0, 0,     # 12: red
    255, 0, 255,   # 13: magenta
    255, 255, 0,   # 14: yellow
    255, 255, 255, # 15: white
]


if __name__ == '__main__':
    proj_name = "city-experiments/3"
    image_paths = list(Path(f"../source-imgs/{proj_name}").glob("*.jpg"))

    for idx, imgpath in enumerate(image_paths[::]):
        photo = Image.open(imgpath)
        w, h = photo.size
        palette_size = 8

        np_photo = np.array(photo)
        np_photo = np_photo.astype(float)


        for i in range(17):
            palette_image = Image.new('P', (1, 1))
            palette = generate_palette(palette_size)
            palette_image.putpalette(palette)

            imgOut = reduce_palette(palette_size, photo, palette)
            imgOut = imgOut.convert("RGB")

            np_palette = np.array(imgOut)
            np_palette = np_palette.astype(float)

            combined = threshold_pixels(np_photo, np_palette, threshold=int(i*10 % 250))
            combined_image = Image.fromarray(np.array(combined))
            combined_image.save(f"../pallette-out/{proj_name}/{idx}-{time()}.jpg")



# if __name__ == '__main__':
#     photo = Image.open("source-imgs/cernovicky-hajek/3.jpg")
#     w, h = photo.size
#     palette_size = 3
#
#     np_photo = np.array(photo)
#     np_photo = np_photo.astype(float)
#
#     palette_image = Image.new('P', (1, 1))
#     palette = generate_palette(palette_size)
#
#     for i in range(128):
#         palette_image.putpalette(palette)
#         palette = vary_palette(palette, 20, 20, 20, 50, 220)
#
#         imgOut = reduce_palette(palette_size, photo, palette)
#         imgOut = imgOut.convert("RGB")
#
#         np_palette = np.array(imgOut)
#         np_palette = np_palette.astype(float)
#
#         threshold = ((sin(i / 8) + 1) * 100)
#
#         print(threshold)
#
#         combined = threshold_pixels(np_photo, np_palette, threshold=int(threshold))
#         combined_image = Image.fromarray(np.array(combined))
#         combined_image.save(f"pallette-out/cernovicky-hajek/{time()}.jpg")

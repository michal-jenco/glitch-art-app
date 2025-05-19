# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image
import numpy as np
from time import time
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


if __name__ == '__main__':
    proj_name = "vlnena"
    image_paths = list(Path(f"../source-imgs/{proj_name}").glob("*.jpg"))

    for idx, imgpath in enumerate(image_paths[::]):
        photo = Image.open(imgpath)
        w, h = photo.size
        palette_size = 8

        np_photo = np.array(photo)
        np_photo = np_photo.astype(float)
        glitches_per_image = 17

        for i in range(glitches_per_image):
            palette_image = Image.new('P', (1, 1))
            palette = generate_palette(palette_size)
            palette_image.putpalette(palette)

            imgOut = reduce_palette(palette_size, photo, palette)
            imgOut = imgOut.convert("RGB")

            np_palette = np.array(imgOut)
            np_palette = np_palette.astype(float)

            combined = threshold_pixels(np_photo, np_palette, threshold=int(i*10 % 250))
            combined_image = Image.fromarray(np.array(combined))
            combined_image.save(f"../pallette-out/{proj_name}/{imgpath.stem}-{i}.jpg")

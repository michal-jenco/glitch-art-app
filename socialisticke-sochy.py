# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image
import numpy as np
from time import time

from helper_functions import generate_palette, reduce_palette, average_rgb_pixel


def iterate_pixels(img_orig, img_palette, threshold: int):
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
    for i in range(10):
        photo = Image.open("source-imgs/sidliskove-sochy/best/1.jpg")
        w, h = photo.size

        palette_size = 7
        pixel_amt = 8

        np_photo = np.array(photo)
        np_photo = np_photo.astype(float)

        palette_image = Image.new('P', (1, 1))
        palette = generate_palette(palette_size)
        palette_image.putpalette(palette)

        imgOut = reduce_palette(palette_size, photo, palette)
        imgOut = imgOut.convert("RGB")

        np_palette = np.array(imgOut)
        np_palette = np_palette.astype(float)

        combined = iterate_pixels(np_photo, np_palette, threshold=110)
        combined_image = Image.fromarray(np.array(combined))
        combined_image.save(f"pallette-out/sidliskove-sochy/{time()}.png")

        x = combined_image.resize(size=(w // pixel_amt, h // pixel_amt * 4), resample=0)
        x = x.resize((w, h), resample=0)
        x.save(f"pallette-out/sidliskove-sochy/{time()}.png")

        combined_image = combined_image.quantize(
            palette=palette_image,
            dither=Image.Dither.FLOYDSTEINBERG,
            kmeans=4,
            method=2,
        )

        combined_image.save(f"pallette-out/sidliskove-sochy/{time()}.png")

        combined_image = combined_image.resize(size=(w // pixel_amt, h // pixel_amt * 4), resample=0)
        combined_image = combined_image.resize((w, h), resample=0)

        combined_image.save(f"pallette-out/sidliskove-sochy/{time()}.png")

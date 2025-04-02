# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image
import numpy as np
from time import time
from pathlib import Path

from helper_functions import generate_palette, reduce_palette, average_rgb_pixel, vary_palette, create_stripes


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
    proj_name = "dead-trees-2025"
    input_imgs_folder = f"source-imgs/{proj_name}"
    output_imgs_folder = f"pallette-out/{proj_name}"
    glitches_per_single_image = 10

    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))
    palette_size = 4

    for i, img_path in (enumerate(input_image_paths)):
        for _ in range(glitches_per_single_image):
            glitched_image = Image.open(img_path)
            w, h = glitched_image.size

            palette = generate_palette(palette_size)

            ### ADD STRIPE COPIES
            create_stripes(
                glitched_image,
                num_of_stripes=(i % 20) + 7,
                stripe_height=((i * 5) % 15) + 7,
            )
            ### ADD STRIPE COPIES

            ### DITHER + PALETTE
            palette_image = Image.new('P', (1, 1))
            palette_image.putpalette(palette)

            glitched_image = glitched_image.quantize(
                palette=palette_image,
                dither=Image.Dither.FLOYDSTEINBERG,
            )
            ### DITHER + PALETTE

            glitched_image = glitched_image.convert("RGB")
            glitched_image.save(f"pallette-out/{proj_name}/{i}-{time()}.jpg")


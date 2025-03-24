# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com

from random import random, randrange

from PIL import Image
from time import time
from pathlib import Path

from helper_functions import (
    create_stripes, threshold_palette, generate_palette, vary_palette,
)
from palettes import retro_palettes, custom_palettes


if __name__ == '__main__':
    images = list(Path("source-imgs/vyletik").glob("*.jpg"))
    num_of_images = len(images)

    glitches_per_single_image = 100
    stripe_size = 30
    palette_size = 5

    for i, image_name in enumerate(images[:]):
        for _ in range(glitches_per_single_image):
            glitched_image = Image.open(image_name)
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

            print(f"Saved image {i}/{num_of_images}")
            glitched_image.save(f"pallette-out/vyletik-report-video/{image_name.stem}-{time()}-{palette}.png")

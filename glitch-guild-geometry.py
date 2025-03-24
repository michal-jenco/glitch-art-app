# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com

from random import  randrange

from PIL import Image
from time import time
from pathlib import Path

from helper_functions import (
    create_stripes, generate_palette, vary_palette, make_tiles
)


if __name__ == '__main__':
    images = list(Path("source-imgs/glitch-guild/geometry").glob("*.jpg"))
    num_of_images = len(images)

    glitches_per_single_image = 35
    stripe_size = 30
    palette_size = 8

    for i, image_name in enumerate(images[:]):
        palette = generate_palette(palette_size)

        palette[0], palette[1], palette[2] = 20, 5, 39
        palette[6], palette[7], palette[8] = 50, 15, 29

        for j in range(glitches_per_single_image):
            glitched_image = Image.open(image_name)
            w, h = glitched_image.size

            glitched_image = glitched_image.rotate(angle=-j * 10)
            palette = vary_palette(palette, 20, 20, 20, 50, 180)

            ### ADD STRIPE COPIES
            create_stripes(
                glitched_image,
                num_of_stripes=30,
                stripe_height=randrange(10, 30),
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

            for cnt in range(15, 80):
                glitched_image = make_tiles(glitched_image, 50)

            print(f"Saved image {i}/{num_of_images}")
            glitched_image.save(f"pallette-out/glitch-guild/geometry/{image_name.stem}-{time()}.png")

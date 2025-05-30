# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com

from random import random, randrange

from PIL import Image, ImageDraw, ImageFont
from math import sin, cos
from pathlib import Path

from helper_functions import (
    create_stripes, threshold_palette, generate_palette, generate_img_with_adaptive_palette,
    vary_palette,
)


if __name__ == '__main__':
    images = list(Path("source-imgs/jpeg-sequences/nokia").glob("*.jpg"))
    num_of_images = len(images)

    stripe_size = 30
    palette_size = 16
    num_of_identical_consecutive_imgs = 3
    consecutive = True

    for i, image_name in enumerate(images[:]):
        glitched_image = Image.open(image_name)
        draw = ImageDraw.Draw(glitched_image, mode="RGBA")

        w, h = glitched_image.size

        eff1 = False
        eff2 = False
        eff3 = False

        palette = generate_palette(palette_size, floor=0, ceiling=215)

        rand_number = random()

        ### ADD STRIPE COPIES
        if rand_number > .1 or eff1:
            eff1 = True
            create_stripes(
                glitched_image,
                num_of_stripes=(i % 20) + 7,
                stripe_height=((i * 5) % 15) + 7,
            )

        ### DITHER + PALETTE
        if rand_number > .1 or eff2:
            eff2 = True

            palette_image = Image.new('P', (1, 1))
            palette_image.putpalette(palette)

            glitched_image = glitched_image.quantize(
                palette=palette_image,
                dither=Image.Dither.FLOYDSTEINBERG,
            )

        ### PALETTE THRESHOLDING
        if rand_number > .3 or eff3:
            eff3 = True
            glitched_image = threshold_palette(glitched_image.convert("RGB"), palette_size, 95, palette=palette)

        if (i % num_of_identical_consecutive_imgs) == 0:
            eff1 = eff2 = eff3 = False
            consecutive = False
        else:
            consecutive = True


        # glitched_image = generate_img_with_adaptive_palette(glitched_image, palette, palette_size, i=i * 8)
        glitched_image = glitched_image.convert("RGB")

        print(f"Saved image {i}/{num_of_images}")
        glitched_image.save(f"pallette-out/nokia/{image_name.stem}.jpg")

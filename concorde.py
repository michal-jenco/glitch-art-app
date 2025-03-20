# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com

from random import randint, random, randrange

from PIL import Image
from time import time
from math import sin
from pathlib import Path
import numpy as np

from helper_functions import create_stripes, threshold_pixels, threshold_palette, generate_palette


def stripe_f(stripe):
    r, g, b = stripe.split()

    r = r.point(lambda i: i * random() * 2)
    g = g.point(lambda i: i * random() * 2)
    b = b.point(lambda i: i * random() * 2)

    stripe = Image.merge('RGB', (r, g, b))

    return stripe


if __name__ == '__main__':
    images = list(Path("source-imgs/jpeg-sequences/concorde").glob("*.jpg"))
    num_of_images = len(images)

    stripe_size = 30
    palette_size = 4
    num_of_identical_consecutive_imgs = 6
    consecutive = True

    palette = generate_palette(palette_size)

    for i, image_name in enumerate(images[:]):
        glitched_image = Image.open(image_name)

        eff1 = False
        eff2 = False
        eff3 = False

        if not consecutive:
            palette = generate_palette(palette_size)

        rand_number = random()

        if rand_number > .4 or eff1:
            eff1 = True
            create_stripes(
                glitched_image,
                num_of_stripes=(i % 20) + 7,
                stripe_height=((i * 5) % 25) + 7,
                stripe_func=stripe_f,
            )

        if rand_number > .5 or eff2:
            eff2 = True

            palette_image = Image.new('P', (1, 1))
            palette_image.putpalette(palette)

            glitched_image = glitched_image.quantize(
                palette=palette_image,
                dither=Image.Dither.FLOYDSTEINBERG,
                kmeans=4,
                method=2,
            )

        if rand_number > .5 or eff3:
            eff3 = True
            glitched_image = threshold_palette(glitched_image.convert("RGB"), palette_size, 95, palette=palette)

        if (i % num_of_identical_consecutive_imgs) == 0:
            eff1 = eff2 = eff3 = False
            consecutive = False
        else:
            consecutive = True


        glitched_image = glitched_image.convert("RGB")
        original_image = Image.open(image_name)

        alpha = randint(5, 10) / 10.
        combined_image = Image.blend(original_image, glitched_image, alpha=alpha)

        print(f"Saved image {i}/{num_of_images}, a={alpha}")
        combined_image.save(f"pallette-out/concorde/{image_name.stem}.jpg")

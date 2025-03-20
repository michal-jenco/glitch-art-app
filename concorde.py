# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com

from random import random, randrange

from PIL import Image, ImageDraw, ImageFont
from math import sin, cos
from pathlib import Path

from helper_functions import create_stripes, threshold_pixels, threshold_palette, generate_palette


def stripe_f(stripe):
    r, g, b = stripe.split()

    r = r.point(lambda i: i * random() * 2)
    g = g.point(lambda i: i * random() * 2)
    b = b.point(lambda i: i * random() * 2)

    stripe = Image.merge('RGB', (r, g, b))

    return stripe


quotes = [
    "The sky is not the limit; it's the beginning of your endless journey.",
    "To fly is to remind yourself that there are no boundaries, only horizons waiting to be explored.",
    "Spread your wings and let your dreams take flight.",
    "The higher you soar, the farther you’ll see.",
    "Flying is not about defying gravity; it’s about embracing freedom.",
    "When you fly, you realize that the impossible is just a matter of perspective.",
    "The wind beneath your wings is the strength of your belief.",
    "Let your spirit soar high, for the world is yours to discover."
]


if __name__ == '__main__':
    images = list(Path("source-imgs/jpeg-sequences/concorde").glob("*.jpg"))
    num_of_images = len(images)

    stripe_size = 30
    palette_size = 4
    num_of_identical_consecutive_imgs = 3
    consecutive = True

    min_alpha, max_alpha = .7, 1

    palette = generate_palette(palette_size)

    for i, image_name in enumerate(images[:]):
        glitched_image = Image.open(image_name)
        draw = ImageDraw.Draw(glitched_image, mode="RGBA")

        w, h = glitched_image.size

        eff1 = False
        eff2 = False
        eff3 = False

        if not consecutive:
            palette = generate_palette(palette_size)

        rand_number = random()

        ### ADD TEXT
        if rand_number > .7:
            for j in range(1, randrange(2, 6)):
                text = quotes[int((i / num_of_images) * len(quotes))]

                draw.text(
                    xy=(randrange(0, w // 3), randrange(0, h)),
                    text=text,
                    font=ImageFont.truetype(
                        "arial",
                        size=randrange(10, 25),
                    ),
                    fill="white",
                    stroke_width=3,
                    stroke_fill='black',
                )

        ### ADD STRIPE COPIES
        if rand_number > .55 or eff1:
            eff1 = True
            create_stripes(
                glitched_image,
                num_of_stripes=(i % 10) + 7,
                stripe_height=((i * 5) % 15) + 7,
                stripe_func=None,
            )

        ### DITHER + PALETTE
        if rand_number > .35 or eff2:
            eff2 = True

            palette_image = Image.new('P', (1, 1))
            palette_image.putpalette(palette)

            glitched_image = glitched_image.quantize(
                palette=palette_image,
                dither=Image.Dither.FLOYDSTEINBERG,
                kmeans=4,
                method=2,
            )

        ### PALETTE THRESHOLDING
        if rand_number > .75 or eff3:
            eff3 = True
            glitched_image = threshold_palette(glitched_image.convert("RGB"), palette_size, 95, palette=palette)

        if (i % num_of_identical_consecutive_imgs) == 0:
            eff1 = eff2 = eff3 = False
            consecutive = False
        else:
            consecutive = True


        glitched_image = glitched_image.convert("RGB")
        # original_image = Image.open(image_name)
        #
        alpha = max(min((cos(i / 15) + 1) / 2, max_alpha), min_alpha)
        # combined_image = Image.blend(original_image, glitched_image, alpha=alpha)

        print(f"Saved image {i}/{num_of_images}, a={alpha}")
        glitched_image.save(f"pallette-out/concorde/{image_name.stem}.jpg")

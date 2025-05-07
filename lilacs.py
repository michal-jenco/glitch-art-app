# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com

import random
from random import randrange, choice, randint

from PIL import Image
from pathlib import Path

from helper_functions import make_tiles

# some good ones I generated randomly
pal_3 = [172, 29, 198, 164, 197, 181, 62, 113, 117, 33, 55, 26, 98, 177, 45, 147, 24, 33, 54, 162, 190]
pal4 = [145, 154, 117, 147, 66, 41, 150, 108, 44, 102, 182, 73, 82, 89, 193, 90, 22, 21, 136, 144, 57]
pal5 = [87, 53, 181, 33, 84, 30, 87, 166, 177, 156, 193, 63, 46, 55, 45, 189, 84, 96, 69, 161, 162]
pal6 = [60, 170, 156, 50, 161, 100, 159, 180, 190, 54, 48, 53, 192, 53, 170, 137, 133, 127, 165, 24, 160]
pal7 = [58, 37, 53, 161, 182, 62, 33, 116, 74, 126, 52, 156, 163, 184, 46, 161, 21, 178, 199, 89, 55]

good_palettes = pal_3, pal4, pal5, pal6, pal7


def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def pregenerate_stripes(num_of_stripes: int, image_size: tuple) -> list:
    w, h = image_size
    stripes = []

    for i in range(num_of_stripes):
        upper = randint(0, h)
        lower = upper + stripe_height

        left, upper, right, lower = 0, upper, w, lower
        box_from = left, upper, right, lower

        upper = randint(0, h)
        lower = upper + stripe_height
        box_to = 0, upper, w, lower

        stripe = [box_from, box_to]
        stripes.append(stripe)
    return stripes


def create_stripes_pregenerated(image: Image, pregenerated_stripes: list):
    for stripe in pregenerated_stripes:
        box_from, box_to = stripe
        stripe = image.crop(box=box_from)

        image.paste(stripe, box=box_to)



if __name__ == '__main__':
    proj_name = "lilac-jpegs"
    input_imgs_folder = f"source-imgs/{proj_name}"
    output_imgs_folder = f"pallette-out/{proj_name}"

    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))

    # palette = generate_palette(7, 255, 50, 200, 20, 200)

    frame_overlap = 3
    palette = choice(good_palettes)
    _base_image = Image.open(input_image_paths[0])
    w, h = _base_image.size
    pregenerated_stripes = []

    ### PREGENERATE STRIPES
    for imgpath in input_image_paths:
        num_of_stripes = randrange(5, 10)
        stripe_height = randrange(15, 40)

        stripes = pregenerate_stripes(num_of_stripes, (w, h))

        for _ in range(frame_overlap):
            pregenerated_stripes.append(stripes)
    ### PREGENERATE STRIPES

    for i, img_path in enumerate(input_image_paths[::]):
        glitched_image = Image.open(img_path)
        w, h = glitched_image.size

        glitched_image = make_tiles(glitched_image, cnt=frame_overlap)

        ### ADD STRIPE COPIES
        create_stripes_pregenerated(
            glitched_image,
            pregenerated_stripes[i],
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

        save_filename = f"pallette-out/{proj_name}/{img_path.stem}-{i}.png"
        print(f"saving {save_filename} - {i}/{len(input_image_paths)}")
        glitched_image.save(save_filename)

        if random.random() > .9:
            palette = choice(good_palettes)

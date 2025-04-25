# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com

import random
from random import randrange, choice, randint

from PIL import Image
from pathlib import Path

from helper_functions import make_tiles


palette_1 = [
    20, 20, 19,
    193, 5, 63,
    199, 61, 69,
    0, 0, 0
]

palette_2 = [
    0, 0, 1,
    89, 0, 34,
    121, 126, 120,
    188, 167, 172,
    201, 153, 215,
]

pal_3 = [172, 29, 198, 164, 197, 181, 62, 113, 117, 33, 55, 26, 98, 177, 45, 147, 24, 33, 54, 162, 190]
pal4 = [145, 154, 117, 147, 66, 41, 150, 108, 44, 102, 182, 73, 82, 89, 193, 90, 22, 21, 136, 144, 57]
pal5 = [87, 53, 181, 33, 84, 30, 87, 166, 177, 156, 193, 63, 46, 55, 45, 189, 84, 96, 69, 161, 162]
pal6 = [60, 170, 156, 50, 161, 100, 159, 180, 190, 54, 48, 53, 192, 53, 170, 137, 133, 127, 165, 24, 160]
pal7 = [58, 37, 53, 161, 182, 62, 33, 116, 74, 126, 52, 156, 163, 184, 46, 161, 21, 178, 199, 89, 55]

good_palettes = pal_3, pal4, pal5, pal6, pal7


lyrics = [
"story goes on",

"is there any way to your heart which is shorter than the way I tried",
"is there any way to your heart which is shorter than the one I tried",

"is there any",
"is there any",
"is there any",

"is there any story",

"my heart"

"is there any way to your heart which is shorter than the way I tried",
"is there any way to your heart which is shorter than I tried",
]


def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]



if __name__ == '__main__':
    proj_name = "moncello-monjur-desert-2025"
    source_folder_name = "any-story-jpegs"
    input_imgs_folder = f"../source-imgs/{proj_name}/{source_folder_name}"
    output_imgs_folder = f"../pallette-out/{proj_name}/{source_folder_name}"

    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))

    # palette = generate_palette(7, 255, 50, 200, 20, 200)

    frame_overlap = 3
    palette = choice(good_palettes)
    base_image = Image.open(input_image_paths[0])
    w, h = base_image.size

    for i, chunk in enumerate(list(chunk_list(input_image_paths, frame_overlap))[:10:]):
        num_of_stripes = randrange(5, 10)
        stripe_height = randrange(15, 40)

        upper_from_list = [randint(0, h) for x in range(frame_overlap)]
        lower_from_list = [upper_from_list[i] + stripe_height for i, x in enumerate(upper_from_list)]

        upper_to_list = [randint(0, h) for x in range(frame_overlap)]
        lower_to_list = [upper_to_list[i] + stripe_height for x in enumerate(upper_to_list)]

        for img_path in chunk:
            glitched_image = Image.open(img_path)
            w, h = glitched_image.size

            ### ADD STRIPE COPIES
            for j in range(num_of_stripes):
                left, upper, right, lower = 0, upper_to_list[j], w, lower_to_list[j]
                box = left, upper_to_list[j], right, lower_to_list[j]
                stripe = glitched_image.crop(box=box)

                glitched_image.paste(stripe, box=(0, upper, w, lower))
            ### ADD STRIPE COPIES

            glitched_image = make_tiles(glitched_image, cnt=frame_overlap)

            ### DITHER + PALETTE
            palette_image = Image.new('P', (1, 1))
            palette_image.putpalette(palette)

            glitched_image = glitched_image.quantize(
                palette=palette_image,
                dither=Image.Dither.FLOYDSTEINBERG,
            )
            ### DITHER + PALETTE

            save_filename = f"../pallette-out/{proj_name}/{source_folder_name}/{img_path.stem}-{i}.png"
            print(f"saving {save_filename} - {i}/{len(input_image_paths)}")
            glitched_image.save(save_filename)

            if random.random() > .9:
                palette = choice(good_palettes)

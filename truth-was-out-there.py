# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com

from random import randrange

from PIL import Image
from pathlib import Path

from helper_functions import generate_palette, vary_palette, create_stripes, darken_palette


sentences = [
    "truth was out there I saw it",
    "truth was out there YOU saw it",
    "truth was out there SHE saw it",
    "truth was out there WE saw it",
    "but nobody said a word",
    "Nobody said a fucking word",
    "So I asked",
    "What is this all about",
    "So I asked",
    "What is this all about",
    "So I asked ",
    "What is this all about",
    "And I kept asking",
    "Because I couldn’t get it",
    "What are we watching",
    "What is this all fucking about",
    "truth was out there I saw it",
    "truth was out there YOU saw it",
    "truth was out there SHE saw it",
    "truth was out there WE saw it",
    "But nobody said a word",
    "Nobody said a fucking word",
    "Nobody said a fucking word",
    "Nobody",
    "Nobody said a fucking word",
    "Nobody",
    "We were silent",
    "What are we watching",
]


# some good ones I generated randomly
pal_3 = [172, 29, 198, 164, 197, 181, 62, 113, 117, 33, 55, 26, 98, 177, 45, 147, 24, 33, 54, 162, 190]
pal4 = [145, 154, 117, 147, 66, 41, 150, 108, 44, 102, 182, 73, 82, 89, 193, 90, 22, 21, 136, 144, 57]
pal5 = [87, 53, 181, 33, 84, 30, 87, 166, 177, 156, 193, 63, 46, 55, 45, 189, 84, 96, 69, 161, 162]
pal6 = [60, 170, 156, 50, 161, 100, 159, 180, 190, 54, 48, 53, 192, 53, 170, 137, 133, 127, 165, 24, 160]
pal7 = [58, 37, 53, 161, 182, 62, 33, 116, 74, 126, 52, 156, 163, 184, 46, 161, 21, 178, 199, 89, 55]

good_palettes = pal_3, pal4, pal5, pal6, pal7


if __name__ == '__main__':
    proj_name = "truth-is-out-there"
    input_imgs_folder = f"source-imgs/{proj_name}/jpeg-exports"
    output_imgs_folder = f"pallette-out/{proj_name}"

    scene_name = "running-1"

    input_image_paths = list(Path(f"{input_imgs_folder}/{scene_name}").glob("*.jpg"))
    palette_size = 7

    palette = generate_palette(palette_size)

    for i, img_path in (enumerate(input_image_paths[::])):
        glitched_image = Image.open(img_path)
        w, h = glitched_image.size

        ### ADD STRIPE COPIES
        create_stripes(
            glitched_image,
            num_of_stripes=randrange(5, 10),
            stripe_height=randrange(15, 50),
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

        save_filename = f"pallette-out/{proj_name}/{img_path.stem}.png"
        print(f"saving {save_filename} - {i}/{len(input_image_paths)}")
        glitched_image.save(save_filename)

        palette = vary_palette(palette, 15, 5, 15)
        palette = darken_palette(palette, 4)

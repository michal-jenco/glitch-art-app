# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com

from random import randrange

from PIL import Image

from helper_functions import (
    make_panned_sequence, PanDirection, create_stripes, generate_palette, vary_palette
)


if __name__ == '__main__':
    project_name = "those-lights-are-dead-stars-dreamcore-poolslide"
    img_index = 2

    image_path = f"source-imgs/{project_name}/{img_index}.png"
    photo = Image.open(image_path)

    panned_seq = make_panned_sequence(photo, PanDirection.LRL, 8, "9:16")
    palette = generate_palette(8)

    for i, slide in enumerate(panned_seq):
        print(f"Saved image {i}/{len(panned_seq)}")

        w, h = slide.size

        ### DITHER + PALETTE
        palette_image = Image.new('P', (1, 1))
        palette_image.putpalette(palette)

        slide = slide.quantize(
            palette=palette_image,
            dither=Image.Dither.FLOYDSTEINBERG,
        )
        ### DITHER + PALETTE

        ### ADD STRIPE COPIES
        create_stripes(
            slide,
            num_of_stripes=randrange(0, 10),
            stripe_height=randrange(10, 20),
        )
        ### ADD STRIPE COPIES

        slide.save(f"pallette-out/{project_name}/{img_index}-{i}.png")

        palette = vary_palette(palette, 15, 15, 15, 0, 225)

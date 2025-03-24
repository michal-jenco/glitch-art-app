# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com
from random import randrange

from PIL import Image

from helper_functions import (
    make_panned_sequence, PanDirection, create_stripes, generate_palette, vary_palette,
)


if __name__ == '__main__':
    image_path = "source-imgs/pan-test1.jpg"
    photo = Image.open(image_path)

    panned_seq = make_panned_sequence(photo, PanDirection.LRL, 5, "4:5")

    palette = generate_palette(8)

    for i, slide in enumerate(panned_seq):
        print(f"Saved image {i}/{len(panned_seq)}")

        ### ADD STRIPE COPIES
        create_stripes(
            slide,
            num_of_stripes=randrange(5, 15),
            stripe_height=randrange(10, 35),
        )
        ### ADD STRIPE COPIES

        ### DITHER + PALETTE
        palette_image = Image.new('P', (1, 1))
        palette_image.putpalette(palette)

        slide = slide.quantize(
            palette=palette_image,
            dither=Image.Dither.FLOYDSTEINBERG,
        )
        ### DITHER + PALETTE

        slide.save(f"pallette-out/pan-test/{i}.png")

        palette = vary_palette(palette, 15, 5, 15, 0, 185)

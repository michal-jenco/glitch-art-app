# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com

from random import randrange

from PIL import Image

from helper_functions import (
    make_panned_sequence, PanDirection, create_stripes, generate_palette, vary_palette, darken_palette
)


if __name__ == '__main__':
    image_path = "source-imgs/scout-girl.jpg"
    photo = Image.open(image_path)

    panned_seq = make_panned_sequence(photo, PanDirection.LRL, 25, "9:16")

    for i, slide in enumerate(panned_seq):
        palette = generate_palette(8)
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
            num_of_stripes=randrange(15, 30),
            stripe_height=randrange(10, 35),
        )
        ### ADD STRIPE COPIES

        slide = slide.resize(size=(w // 4, h // 4), resample=0)

        slide.save(f"pallette-out/scout-girl/{i}.png")

        # palette = vary_palette(palette, 15, 15, 15, 0, 225)
        palette = darken_palette(palette)

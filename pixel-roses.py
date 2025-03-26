# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from random import  randrange
from PIL import Image
from time import time

from helper_functions import create_stripes, generate_palette, vary_palette


if __name__ == '__main__':
    palette_size = 7
    pixelation = 4

    for i in range(20):
        image = Image.open("source-imgs/roses/5.jpg")
        palette = generate_palette(palette_size, floor=0, ceiling=185)

        w, h = image.size
        palette = vary_palette(palette, 15, 15, 15, 10, 220)

        ### DARKEN THE PALETTE
        for j, _ in enumerate(palette):
            if j % 4 == 0:
                palette[j] = randrange(15, 35)
        ### DARKEN THE PALETTE

        ### ADD STRIPE COPIES
        create_stripes(
            image,
            num_of_stripes=10,
            stripe_height=randrange(10, 30),
        )
        ### ADD STRIPE COPIES

        ### DITHER + PALETTE
        palette_image = Image.new('P', (1, 1))
        palette_image.putpalette(palette)

        image = image.quantize(palette=palette_image, dither=Image.Dither.FLOYDSTEINBERG)
        ### DITHER + PALETTE

        ### PIXELATE
        image = image.resize(size=(w // pixelation, h // pixelation), resample=0)
        image = image.resize((w, h), resample=0)
        ### PIXELATE

        save_path = f"pallette-out/roses/{time()}.png"
        print(f"Saving {save_path}")
        image.save(save_path)

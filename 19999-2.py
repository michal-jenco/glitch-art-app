# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from random import randrange

from PIL import Image
from time import time
from pathlib import Path

from helper_functions import generate_palette, vary_palette, create_stripes



if __name__ == '__main__':
    proj_name = "19999-2"
    input_imgs_folder = f"source-imgs/{proj_name}"
    output_imgs_folder = f"pallette-out/{proj_name}"

    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))
    palette_size = 8

    palette = generate_palette(palette_size)
    upscale_x = 3

    for i, img_path in (enumerate(input_image_paths[5005:])):
        glitched_image = Image.open(img_path)
        w, h = glitched_image.size

        ### ADD STRIPE COPIES
        create_stripes(
            glitched_image,
            num_of_stripes=randrange(5, 10),
            stripe_height=randrange(5, 20),
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

        glitched_image = glitched_image.resize((w * upscale_x, h * upscale_x), resample=0)
        glitched_image.save(f"pallette-out/{proj_name}/{img_path.stem}-{time()}.png")

        palette = vary_palette(palette, 20, 10, 30)

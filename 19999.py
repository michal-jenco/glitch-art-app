# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image
import numpy as np
from time import time
from pathlib import Path

from helper_functions import generate_palette, vary_palette, create_stripes



if __name__ == '__main__':
    proj_name = "19999"
    input_imgs_folder = f"source-imgs/{proj_name}"
    output_imgs_folder = f"pallette-out/{proj_name}"

    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))
    palette_size = 4

    palette = generate_palette(palette_size)

    for i, img_path in (enumerate(input_image_paths)):
        glitched_image = Image.open(img_path)
        w, h = glitched_image.size

        ### ADD STRIPE COPIES
        create_stripes(
            glitched_image,
            num_of_stripes=(i % 20),
            stripe_height=((i * 5) % 15) + 7,
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

        glitched_image.save(f"pallette-out/{proj_name}/{img_path.stem}-{time()}.png")

        palette = vary_palette(palette, 20, 10, 30)

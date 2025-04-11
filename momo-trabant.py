# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from random import randrange

from PIL import Image
from time import time
from pathlib import Path

from helper_functions import generate_palette, vary_palette, create_stripes



if __name__ == '__main__':
    proj_name = "momo-trabant"
    input_imgs_folder = f"source-imgs/jpeg-sequences/{proj_name}"
    output_imgs_folder = f"pallette-out/{proj_name}"

    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))
    palette_size = 16

    palette = generate_palette(palette_size)
    upscale_x = 2

    for i, img_path in (enumerate(input_image_paths[::])):
        glitched_image = Image.open(img_path)
        w, h = glitched_image.size

        ### ADD STRIPE COPIES
        create_stripes(
            glitched_image,
            num_of_stripes=randrange(5, 20),
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

        # glitched_image = glitched_image.resize((w // upscale_x, h // upscale_x), resample=0)
        # glitched_image = glitched_image.resize((w, h), resample=0)

        save_filename = f"pallette-out/{proj_name}/{img_path.stem}-{time()}.png"
        print(f"saving {save_filename} - {i}/{len(input_image_paths)}")
        glitched_image.save(save_filename)

        palette = vary_palette(palette, 15, 5, 15)

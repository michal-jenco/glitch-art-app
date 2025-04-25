# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from random import randrange

from PIL import Image
from time import time
from pathlib import Path

from helper_functions import generate_palette, vary_palette, create_stripes, darken_palette



if __name__ == '__main__':
    proj_name = "moncello-monjur-desert-2025"
    source_folder_name = "any-story-jpegs"
    input_imgs_folder = f"source-imgs/{proj_name}/{source_folder_name}"
    output_imgs_folder = f"pallette-out/{proj_name}/{source_folder_name}"

    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))
    palette_size = 7

    palette = generate_palette(palette_size)
    upscale_x = 2

    for i, img_path in (enumerate(input_image_paths[:])):
        glitched_image = Image.open(img_path)
        w, h = glitched_image.size

        ### ADD STRIPE COPIES
        create_stripes(
            glitched_image,
            num_of_stripes=randrange(5, 10),
            stripe_height=randrange(15, 40),
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
        # glitched_image = glitched_image.resize((w * upscale_x, h * upscale_x), resample=0)

        save_filename = f"pallette-out/{proj_name}/{source_folder_name}/{img_path.stem}-{i}.png"
        print(f"saving {save_filename} - {i}/{len(input_image_paths)}")
        glitched_image.save(save_filename)

        palette = vary_palette(palette, 20, 10, 30)
        palette = darken_palette(palette)

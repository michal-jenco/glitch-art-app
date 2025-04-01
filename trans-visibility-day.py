# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from random import  randrange

from PIL import Image
import os
from pathlib import Path

from helper_functions import create_stripes, make_panned_sequence, PanDirection
from palettes import trans_flag_palette


if __name__ == '__main__':
    project_name = "trans-visibility-day"
    src_folder = f"source-imgs/{project_name}"
    image_paths = list(Path(src_folder).glob("*.jpg"))
    images = [Image.open(image_path) for image_path in image_paths]

    for i, img in enumerate(images):
        pan_series = make_panned_sequence(img, PanDirection.LEFT_RIGHT, 20, "4:5")

        for j, slide in enumerate(pan_series):
            w, h = slide.size

            ### ADD STRIPE COPIES
            create_stripes(
                slide,
                num_of_stripes=10,
                stripe_height=randrange(10, 30),
            )
            ### ADD STRIPE COPIES

            ### DITHER + PALETTE
            palette_image = Image.new('P', (1, 1))
            palette_image.putpalette(trans_flag_palette)

            slide = slide.quantize(palette=palette_image, dither=Image.Dither.RASTERIZE)
            ### DITHER + PALETTE

            save_path = f"pallette-out/{project_name}/{i}-{j}.png"
            print(f"Saving {save_path}")
            slide.save(save_path)

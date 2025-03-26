# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com

from random import  randrange

from PIL import Image
import os
from pathlib import Path

from helper_functions import (
    create_stripes, generate_palette, vary_palette, make_panned_sequence_list, PanDirection,
)
from palettes import custom_palettes


if __name__ == '__main__':
    src_folder = "source-imgs/glitch-guild/flowers"
    series_dirs = [f.path for f in os.scandir(src_folder) if f.is_dir()]

    palette_size = 7
    pixelation = 4

    for s, series_dir in enumerate(series_dirs):
        image_paths = list(Path(series_dir).glob("*.jpg"))

        images = [Image.open(image_path) for image_path in image_paths]
        num_of_images = len(images)

        palette = generate_palette(palette_size, floor=0, ceiling=185)

        pan_series = make_panned_sequence_list(images, PanDirection.LRL, 20, "3:4")

        for i, slide in enumerate(pan_series):
            w, h = slide.size
            palette = vary_palette(palette, 15, 15, 15, 10, 220)
            for j, _ in enumerate(palette):
                if j % 4 == 0:
                    palette[j] = randrange(15, 35)

            ### ADD STRIPE COPIES
            create_stripes(
                slide,
                num_of_stripes=10,
                stripe_height=randrange(10, 30),
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

            slide = slide.resize(size=(w // pixelation, h // pixelation), resample=0)
            # and scale it up to get pixelate effect
            slide = slide.resize((w, h), resample=0)

            save_path = f"pallette-out/glitch-guild/flowers-pixel/s{s}-{i}.png"
            print(save_path)
            slide.save(save_path)

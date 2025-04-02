# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from pathlib import Path
from random import randrange
from time import time

from PIL import Image

from helper_functions import generate_palette



if __name__ == '__main__':
    proj_name = "pixel-osaka"
    input_imgs_folder = f"source-imgs/osaka azumanga daioh"
    output_imgs_folder = f"pallette-out/{proj_name}"

    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))

    blowup = 5

    for pal_size in range(3, 12):
        for i, img_path in (enumerate(input_image_paths)):
            im = Image.open(img_path)
            w, h = im.size

            ### DITHER + PALETTE
            palette = generate_palette(pal_size)
            palette_image = Image.new('P', (1, 1))
            palette_image.putpalette(palette)

            im = im.quantize(palette=palette_image, dither=Image.Dither.RASTERIZE)
            ### DITHER + PALETTE

            ### PIXELATE
            im = im.resize((w * blowup, h * blowup), resample=0)
            ### PIXELATE

            im.save(f"{output_imgs_folder}/{i}-{time()}-palsize={pal_size}.png")

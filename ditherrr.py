# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image

from helper_functions import generate_palette


if __name__ == '__main__':
    photo = Image.open("source-imgs/sky-sign.jpg")
    w, h = photo.size

    pixelate_level = 16

    # Make tiny palette Image, one black pixel
    palIm = Image.new('P', (1,1))
    palette = generate_palette(4)
    palIm.putpalette(palette)

    # scale it down
    photo = photo.resize(size=(w // pixelate_level, h // pixelate_level), resample=0)
    # and scale it up to get pixelate effect
    photo = photo.resize((w, h), resample=0)

    # photo = photo.quantize(palette=palIm, dither=Image.Dither.FLOYDSTEINBERG)
    # Quantize actual image to palette



    photo.show()
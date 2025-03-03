# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image, ImageFont, ImageDraw
from time import time

from numpy.random import randint

from helper_functions import generate_palette


if __name__ == '__main__':
    photo = Image.open("source-imgs/moon.jpg")
    draw = ImageDraw.Draw(photo, mode="RGBA")
    w, h = photo.size

    num_of_frames = 70
    palette_size = 16
    words = "this", "is", "how", "I", "see", "you", "btw"
    word_count = len(words)
    col_width = w // word_count

    assert num_of_frames >= word_count

    for i in range(num_of_frames):
        word_idx = i // (num_of_frames // word_count)
        starting_x_pos = word_idx * col_width

        x = int(randint(starting_x_pos, col_width + starting_x_pos))
        y = int(randint(0, h))

        text = words[word_idx]

        draw.text(
            xy=(x, y),
            text=text,
            font=ImageFont.truetype("arial", randint(20, 40)),
        )

        palIm = Image.new('P', (1, 1))
        palette = generate_palette(palette_size)
        palIm.putpalette(palette)

        imgOut = photo.quantize(palette=palIm, dither=Image.Dither.ORDERED)

        imgOut.save(f"pallette-out/moon-how-i-see-you/frames/moon-{int(time())}-frame{i}.png")

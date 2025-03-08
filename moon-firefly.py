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

    num_of_frames = 28 * 4
    palette_size = 14
    words = "this", "is", "how", "I", "see", "you", "btw"
    word_count = len(words)
    col_width = w // word_count

    assert num_of_frames >= word_count

    starting_y = 30

    for i in range(num_of_frames):
        word_idx = i // (num_of_frames // word_count)
        starting_x_pos = word_idx * col_width

        ### random column positions algo
        # x = int(randint(starting_x_pos, col_width + starting_x_pos))
        # y = int(randint(0, h))
        ### random column positions algo

        x = int(randint(starting_x_pos, col_width + starting_x_pos))
        y = (starting_y + i * 30) % h
        text = words[word_idx]

        draw.text(
            xy=(x, y),
            text=text,
            font=ImageFont.truetype("arial", randint(10, 40)),
            fill="#ff007f",
            stroke_width=2,
            stroke_fill='white'
        )

        palIm = Image.new('P', (1, 1))
        palette = generate_palette(palette_size)
        palIm.putpalette(palette)

        imgOut = photo.quantize(palette=palIm, dither=Image.Dither.ORDERED)

        imgOut.save(f"pallette-out/moon-how-i-see-you/frames2/moon-{int(time())}-frame{i}.png")

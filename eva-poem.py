# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from random import randrange

from PIL import Image, ImageDraw, ImageFont
from time import time

from helper_functions import generate_palette


class TextMode:
    WORDS = 0
    LETTERS = 1


def draw_stripe_of_text(text: str, draw: ImageDraw, mode: TextMode, w: int, h: int) -> None:
    x = randrange(20, w - 20)
    y_base = None
    iterator = None

    if mode == TextMode.WORDS:
        iterator = text.split()
        y_base = randrange(20, h - 200)
        text_size = 30 + randrange(-5, 40)

        for i, word in enumerate(iterator):
            y = i * 50 + y_base

            draw.text(
                xy=(x, y),
                text=word,
                font=ImageFont.truetype("fonts/modernoir/bold.ttf", text_size),
                fill="#f0c07f",
                stroke_width=3,
                stroke_fill='blue',
            )

    elif mode == TextMode.LETTERS:
        iterator = text
        y_base = randrange(20, 100)
        text_size = 30 + randrange(-15, 10)

        for i, word in enumerate(iterator):
            y = i * 30 + y_base

            draw.text(
                xy=(x, y),
                text=word,
                font=ImageFont.truetype("fonts/modernoir/regular.ttf", text_size),
                fill="#f0c07f",
                stroke_width=3,
                stroke_fill='blue',
            )



if __name__ == '__main__':
    palette_size = 5

    lines = [
        f"The friendly hand was well extended ",
        f"It placed flowers in my pocket, tapped me on the shoulder ",
        f"But never truly touched my palm",
    ]


    for i in range(0, 64):
        photo = Image.open("source-imgs/eva/2.jpg")
        w, h = photo.size
        draw = ImageDraw.Draw(photo, mode="RGBA")

        x = 10
        y = 100

        for i in range(3):
            draw_stripe_of_text(lines[0], draw, TextMode.LETTERS, w, h)
            draw_stripe_of_text(lines[0], draw, TextMode.LETTERS, w, h)
            draw_stripe_of_text(lines[0], draw, TextMode.WORDS, w, h)

        palIm = Image.new('P', (1, 1))
        palette = generate_palette(palette_size)
        palIm.putpalette(palette)

        imgOut = photo.quantize(palette=palIm, dither=Image.Dither.ORDERED)

        imgOut.save(f"pallette-out/eva/eva-poem1-{time()}-{i}.png")



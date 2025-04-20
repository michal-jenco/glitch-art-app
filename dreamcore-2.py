# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com

from random import randrange, randint

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from blend_modes import blending_functions
from time import time

from helper_functions import generate_palette, generate_stripes_overlay, create_stripes


sentences = [
    "why dont you trust me?",
    "do you really think im only interested in your body?",
    "i get it, youre just being cautious",
    "hope i can prove it to you one day",
]

def draw_text_with_border(image, text, position, font_path=None, font_size=40, text_color="white", border_color="red", output_path="output.png"):
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("arial", 55)

    # Calculate the text size
    text_size = draw.textbbox(position, text, font=font)
    left, top, right, bottom = text_size
    padding = 10  # add some padding around the box

    # Draw the rectangle
    draw.rectangle(
        [left - padding, top - padding, right + padding, bottom + padding],
        outline=border_color,
        width=15
    )

    # Draw the text
    draw.text(position, text, font=font, fill=text_color)

    # Save the result
    # image.save(output_path)
    print(f"Image saved to {output_path}")

def draw_words_with_arrows(image,
                           words,
                           font_size=32,
                           text_color="white",
                           border_color="red",
                           arrow_color="cyan"):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial", font_size)

    width, height = image.size
    positions = []
    boxes = []

    # Draw each word at a random position
    for word in words.split():
        max_attempts = 100
        while max_attempts > 0:
            x = randint(0, width - 100)
            y = randint(0, height - 40)
            text_bbox = draw.textbbox((x, y), word, font=font)
            text_box = [text_bbox[0]-8, text_bbox[1]-4, text_bbox[2]+8, text_bbox[3]+4]

            # Check for overlaps with existing boxes
            if not any((box[0] < text_box[2] and box[2] > text_box[0] and
                        box[1] < text_box[3] and box[3] > text_box[1]) for box in boxes):
                break
            max_attempts -= 1

        draw.rectangle(text_box, outline=border_color, width=5)
        draw.text((x, y), word, fill=text_color, font=font)
        center = ((text_box[0] + text_box[2]) // 2, (text_box[1] + text_box[3]) // 2)
        positions.append(center)
        boxes.append(text_box)

    # Draw arrows (lines with little "arrowheads")
    for i in range(len(positions) - 1):
        start = positions[i]
        end = positions[i + 1]
        draw.line([start, end], fill=arrow_color, width=5)

        # Arrowhead
        dx, dy = end[0] - start[0], end[1] - start[1]
        length = (dx**2 + dy**2) ** 0.5
        if length == 0:
            continue
        ux, uy = dx / length, dy / length
        # Points of the arrowhead
        left = (end[0] - 10 * ux + 5 * uy, end[1] - 10 * uy - 5 * ux)
        right = (end[0] - 10 * ux - 5 * uy, end[1] - 10 * uy + 5 * ux)
        draw.polygon([end, left, right], fill=arrow_color)

    return image


if __name__ == '__main__':
    for sentence in sentences:
        photo = Image.open("source-imgs/dreamcore-2/1.jpg")
        w, h = photo.size

        colors = generate_palette(8, group=True)

        effects = generate_stripes_overlay(w, h, 20, 50, 5, colors)

        np_photo = np.array(photo)
        # append alpha channel
        np_photo = np.dstack((np_photo, np.ones((np_photo.shape[0], np_photo.shape[1], 1)) * 255))
        np_photo = np_photo.astype(float)

        np_effect = np.array(effects)
        # append alpha channel
        np_effect = np_effect.astype(float)

        # imgOut = blending_functions.difference(np_photo, np_effect, 1.0)

        # Save images
        imgOut = np.uint8(np_photo)
        imgOut = Image.fromarray(imgOut)

        # imgOut.save(f"pallette-out/dreamcore-2/{time()}.png")

        palIm = Image.new('P', (1, 1))
        palette = generate_palette(17)
        palIm.putpalette(palette)

        ## DITHER + PALETTE
        palette_image = Image.new('P', (1, 1))
        palette_image.putpalette(palette)

        imgOut = imgOut.convert("RGB")
        imgOut = imgOut.quantize(
            palette=palette_image,
            dither=Image.Dither.FLOYDSTEINBERG,
        )
        ## DITHER + PALETTE

        # draw_text_with_border(imgOut, "AAAAA", position=(w // 2 - 400, h // 2), font_size=250)

        imgOut = draw_words_with_arrows(imgOut, sentence, arrow_color="red", font_size=100)
        imgOut.save(f"pallette-out/dreamcore-2/{time()}.png")

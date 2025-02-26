# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image
import numpy as np
from blend_modes import blending_functions

from helper_functions import generate_palette, generate_stripes_overlay

if __name__ == '__main__':
    photo = Image.open("source-imgs/sky-sign.jpg")
    w, h = photo.size

    # draw.text(
    #     xy=(w // 2 - 400, h // 2),
    #     text="why do you hate me", font=ImageFont.truetype("arial", 150))

    colors = generate_palette(8, group=True)

    effects = generate_stripes_overlay(w, h, 20, 150, 5, colors)

    np_photo = np.array(photo)
    # append alpha channel
    np_photo = np.dstack((np_photo, np.ones((np_photo.shape[0], np_photo.shape[1], 1)) * 255))
    np_photo = np_photo.astype(float)

    np_effect = np.array(effects)
    # append alpha channel
    np_effect = np_effect.astype(float)

    imgOut = blending_functions.difference(np_photo, np_effect, 1.0)

    # Save images
    imgOut = np.uint8(imgOut)
    imgOut = Image.fromarray(imgOut)
    imgOut.show()
# mostly made by chatgpt

import cv2
import numpy as np
from PIL import Image, ImageDraw
from pathlib import Path
import math
from time import time
from random import choice

from palettes import basic_colors


def spiral_polar_glitch(pil_img, intensity=10):
    # Convert PIL to OpenCV
    img = np.array(pil_img.convert("RGB"))
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    max_radius = min(center)

    # Convert to polar coordinates
    polar = cv2.linearPolar(img, center, max_radius, cv2.WARP_FILL_OUTLIERS)

    # Apply sinusoidal distortion along the radial axis
    for i in range(polar.shape[0]):
        shift = int(np.sin(i / intensity) * 15)
        polar[i] = np.roll(polar[i], shift, axis=0)

    # Convert back to Cartesian
    glitched = cv2.linearPolar(polar, center, max_radius, cv2.WARP_FILL_OUTLIERS + cv2.WARP_INVERSE_MAP)

    return Image.fromarray(glitched)


def overlay_colored_squares(img, square_size=50, opacity=80):
    img = img.convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    width, height = img.size

    for x in range(0, width, square_size):
        for y in range(0, height, square_size):
            # color = (
            #     np.random.randint(100, 255),
            #     np.random.randint(100, 255),
            #     np.random.randint(100, 255),
            #     opacity
            # )

            color = *choice(basic_colors), opacity
            draw.rectangle(
                [x, y, x + square_size, y + square_size],
                fill=color
            )

    return Image.alpha_composite(img, overlay).convert("RGB")


def apply_pixel_sort(image, angle=0, degree=20):
    img = image.convert("RGB")
    arr = np.array(img)
    h, w, _ = arr.shape
    output = np.zeros_like(arr)

    angle_rad = math.radians(angle)
    dx = math.cos(angle_rad)
    dy = math.sin(angle_rad)

    for y in range(h):
        for x in range(w):
            line = []
            for i in range(degree):
                sx = int(x + dx * i)
                sy = int(y + dy * i)
                if 0 <= sx < w and 0 <= sy < h:
                    line.append(arr[sy, sx])
            if len(line) > 0:
                sorted_line = sorted(line, key=lambda p: sum(p))
                for i, pixel in enumerate(sorted_line):
                    sx = int(x + dx * i)
                    sy = int(y + dy * i)
                    if 0 <= sx < w and 0 <= sy < h:
                        output[sy, sx] = pixel
    return Image.fromarray(output)


input_imgs_folder = f"../source-imgs/vary-aesthetic/spiral/"
input_image_paths = list(Path(input_imgs_folder).glob("*.png"))

print(input_image_paths)

for i, img_path in enumerate(input_image_paths[::]):
    img = Image.open(img_path)
    glitched = spiral_polar_glitch(img)
    glitched = overlay_colored_squares(glitched)
    final = apply_pixel_sort(glitched, angle=i*10)

    img_save_name = f"../pallette-out/vary-aesthetic/spiral/{int(time())}-{i}.png"
    final.save(img_save_name)

    # final.show()
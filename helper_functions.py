from random import randint

from PIL import ImagePalette, Image, ImageDraw
import random
from typing import Any
import numpy as np


def generate_palette(
        size: int,
        red_amount: float = 1.0,
        green_amount: float = 1.0,
        blue_amount: float = 1.0,
        floor: int = 0,
        ceiling: int = 255,
        group: bool = False,
) -> ImagePalette:

    palette = []

    for i in range(0, size):
        r = random.randint(0 + floor, int(min(255 * red_amount, ceiling)))
        g = random.randint(0 + floor, int(min(255 * green_amount, ceiling)))
        b = random.randint(0 + floor, int(min(255 * blue_amount, ceiling)))

        if group:
            palette.append((r, g, b))
        else:
            palette.append(r)
            palette.append(g)
            palette.append(b)

    return palette


def shift_rgb(img: Image, pixels: Any):
    width, height = img.size

    for w in range(0, width):
        for h in range(0, height):
            r, g, b = pixels[w, h]
            pixels[w, h] = g, b, r

    return img

# def save_image_with_cv2(img: Image.Image, name: str, format: str = "png"):
#     image_array = np.array(img)
#     image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
#     cv2.imwrite(f"{name}.{format}", image_array)


def euclidean_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    p1 = np.array(p1)
    p2 = np.array(p2)

    dist = np.linalg.norm(p1 - p2)

    return float(dist)


def get_image_center_coord(width: int, height: int) -> tuple[int, int]:
    return width // 2, height // 2


def generate_circle_mask(size: tuple[int, int], feather: int, max_mask: int = 255):
    mask = Image.new(mode="RGBA", size=size)

    width, height = mask.size

    center = get_image_center_coord(*mask.size)


    for w in range(0, width):
        for h in range(0, height):
            coord = (w, h)
            dist = int(euclidean_distance(coord, center) / feather)
            pixel_value = min(dist, max_mask)

            mask.putpixel(coord, (pixel_value, pixel_value, pixel_value, pixel_value))

    mask.show()
    # mask.save("C:/Users/misko/PycharmProjects/glitch-art-app/masks/mask2.PNG")

    return mask


def reduce_palette(palette_size: int, img: Any, palette):
    new_img = img.convert("P", palette=Image.ADAPTIVE, colors=palette_size)
    new_img = new_img.convert("P", palette=palette, colors=palette_size)
    new_img.putpalette(palette)

    return new_img

def average_rgb_pixel(r, g, b) -> int:
    return (r + g + b) // 3


def convert_image_to_rgba(img: Image) -> Image:
    width, height = img.size

    for w in range(0, width):
        for h in range(0, height):
            coord = (w, h)
            r, g, b, a = img.getpixel(coord)

            a = (r + g + b) // 3

            img.putpixel(coord, (r, g, b, a))
    img.show()
    # img.save("masks/man_rgba2.png")

def mask_images(img1: Image, img2: Image, mask: Image) -> Image:
    return Image.composite(img1, img2, mask)


def get_math_fname(func) -> str:
    return str(func).split()[-1][:-1]

# generate_circle_mask((1536, 2048), feather=1.5)
# convert_image_to_rgba(Image.open("masks/man.png"))

def generate_stripes_overlay(
        width: int,
        height: int,
        min_w: int,
        max_w: int,
        num_of_stripes: int,
        colors: tuple[tuple],
) -> Image:
    image = Image.new(size=(width, height), mode="RGBA")
    draw = ImageDraw.Draw(image, mode="RGBA")

    for i in range(num_of_stripes):
        color = colors[i % len(colors)]

        x_from = randint(0, width) + min_w
        x_to = randint(x_from, x_from + max_w)

        draw.rectangle(((x_from, 0), (x_to, height)), fill=color)

    return image


def vary_palette(palette, r_amount, g_amount, b_amount, floor, ceiling) -> list:
    changed_palette = []
    amounts = r_amount, g_amount, b_amount

    for i, subpixel in enumerate(palette):
        orig = amounts[i % 3]

        offset = randint(-orig, orig)

        new_color = max(floor, min(subpixel + offset, ceiling))

        changed_palette.append(new_color)
    return changed_palette


def create_stripes(image: Image, num_of_stripes: int, stripe_height: int):
    for i in range(num_of_stripes):
        upper = randint(0, image.height)
        lower = upper + stripe_height

        left, upper, right, lower = 0, upper, image.width, lower
        box = (left, upper, right, lower)
        stripe = image.crop(box=box)

        upper = randint(0, image.height)
        lower = upper + stripe_height
        image.paste(stripe, box=(0, upper, image.width, lower))


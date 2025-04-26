# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from random import randint

from PIL import ImagePalette, Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
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


def vary_palette(palette, r_amount=15, g_amount=15, b_amount=15, floor=0, ceiling=255) -> list:
    changed_palette = []
    amounts = r_amount, g_amount, b_amount

    for i, subpixel in enumerate(palette):
        orig = amounts[i % 3]

        offset = randint(-orig, orig)

        new_color = max(floor, min(subpixel + offset, ceiling))

        changed_palette.append(new_color)
    return changed_palette


def create_stripes(image: Image, num_of_stripes: int, stripe_height: int, stripe_func = None):
    for i in range(num_of_stripes):
        upper = randint(0, image.height)
        lower = upper + stripe_height

        left, upper, right, lower = 0, upper, image.width, lower
        box = (left, upper, right, lower)
        stripe = image.crop(box=box)

        if stripe_func:
            stripe = stripe_func(stripe)

        upper = randint(0, image.height)
        lower = upper + stripe_height
        image.paste(stripe, box=(0, upper, image.width, lower))


# def create_same_stripes_for_x_images(size, images: list[Image], num_of_stripes: int, stripe_height: int,):
#     w, h = size
#
#     upper = randint(0, h)
#     lower = upper + stripe_height
#
#     for image in images:
#         for i in range(num_of_stripes):
#             left, upper, right, lower = 0, upper, w, lower
#             box = (left, upper, right, lower)
#             stripe = image.crop(box=box)
#
#             upper = randint(0, image.height)
#             lower = upper + stripe_height
#             image.paste(stripe, box=(0, upper, image.width, lower))
#
#
# def create_stripes_multiframe(image: Image, num_of_stripes: int, stripe_height: int, frame_overlap: int = 3):
#     upper = randint(0, image.height)
#     lower = upper + stripe_height
#
#     for i in range(num_of_stripes):
#         left, upper, right, lower = 0, upper, image.width, lower
#         box = left, upper, right, lower
#         stripe = image.crop(box=box)
#
#         image.paste(stripe, box=(0, upper, image.width, lower))
#
#         if i % frame_overlap == 0:
#             upper = randint(0, image.height)
#             lower = upper + stripe_height


def threshold_pixels(img_orig, img_palette, threshold: int):
    out = []

    for orig_row, palette_row in zip(img_orig, img_palette):
        row = []

        for orig_pixel, palette_pixel in zip(orig_row, palette_row):
            avg_orig = average_rgb_pixel(*orig_pixel)

            if avg_orig < threshold:
                row.append(orig_pixel)
            else:
                row.append(palette_pixel)

        out.append(row)
    return np.uint8(out)


def threshold_palette(
        photo: Image,
        palette_size: int,
        threshold: int,
        palette: tuple | None = None
) -> Image:
    np_photo = np.array(photo)
    np_photo = np_photo.astype(float)

    if not palette:
        palette = generate_palette(palette_size)
    palette_image = Image.new('P', (1, 1))
    palette_image.putpalette(palette)

    imgOut = reduce_palette(palette_size, photo, palette)
    imgOut = imgOut.convert("RGB")

    np_palette = np.array(imgOut)
    np_palette = np_palette.astype(float)

    combined = threshold_pixels(np_photo, np_palette, threshold=threshold)
    combined_image = Image.fromarray(np.array(combined))

    return combined_image


def glitch_pixels(img: Image.Image, i: int) -> Image:
    width, height = img.size
    pixel_image = img.convert("RGB")

    for w in range(0, width):
        for h in range(0, height):
            r, g, b = pixel_image.getpixel((w, h))

            modified_pixel = displacement_func(r, g, b, w, h, i)
            pixel_image.putpixel((w, h), modified_pixel)

    return pixel_image


def displacement_func(r, g, b, h, w, i) -> tuple:
    new_r = (r + (w % 25)) % 255
    new_g = (g + h) % 200
    new_b = (b + h + w) // 60 % 255

    return new_r, new_g, new_b


def generate_img_with_adaptive_palette(img, palette: ImagePalette, palette_size: int, i: int):
    img = glitch_pixels(img, i)
    img = reduce_palette(palette_size, img, palette)
    return img


def make_tiles(photo: Image, cnt: int):
    w, h = photo.size

    for i in range(cnt):
        tile_step = random.randrange(10, 35)
        tile_w, tile_h = random.randrange(50, 200), random.randrange(50, 200)

        left = random.randrange(0, w)
        upper = random.randrange(0, h)
        right = left + tile_w
        lower = upper + tile_h

        box = left, upper, right, lower

        tile = photo.crop(box=box)

        sign1 = random.choice([-1, 1, 0])
        sign2 = random.choice([-1, 1, 0])
        weight1 = random.random()
        weight2 = random.random()

        for i in range(random.randrange(5, 50)):
            x = left + i * sign1 * weight1 * tile_step ** 1.2
            y = upper + i * sign2 * weight2 * tile_step ** .8

            photo.paste(tile, (int(x), int(y)))

        return photo


class PanDirection:
    LEFT_RIGHT = 0
    RIGHT_LEFT = 1
    LRL = 2
    RLR = 3


def make_panned_sequence(image: Image,
                         direction: PanDirection,
                         step_size: int,
                         aspect_ratio: str
                         ) -> list[Image]:
    """
    :param image:
    :param direction:
    :param step_size:
    :param aspect_ratio: Need to be string in the format "x:y", e.g. 4:5 for instagram
    :return:
    """

    w, h = image.size

    x_ratio, y_ratio = aspect_ratio.split(":")
    x_ratio, y_ratio = int(x_ratio), int(y_ratio)

    output_sequence: list[Image] = []
    slide_width = int(h / y_ratio * x_ratio)

    left, upper, right, lower = 0, 0, slide_width, h

    while True:
        box = left, upper, right, lower
        slide = image.crop(box)

        output_sequence.append(slide)

        left += step_size
        right += step_size

        if right > w:
            break

    if direction == PanDirection.LEFT_RIGHT:
        return output_sequence
    elif direction == PanDirection.RIGHT_LEFT:
        output_sequence.reverse()

        return output_sequence
    elif direction == PanDirection.LRL:
        reversed_copy = output_sequence.copy()
        reversed_copy.reverse()

        return output_sequence[:-1] + reversed_copy


def make_panned_sequence_list(images: list[Image],
                              direction: PanDirection,
                              step_size: int,
                              aspect_ratio: str
                              ) -> list[Image]:
    """
    :param images: All need to be the exact same dimensions
    :param aspect_ratio: Need to be string in the format "x:y", e.g. 4:5 for instagram
    """
    w, h = images[0].size

    x_ratio, y_ratio = aspect_ratio.split(":")
    x_ratio, y_ratio = int(x_ratio), int(y_ratio)

    output_sequence: list[Image] = []
    slide_width = int(h / y_ratio * x_ratio)

    left, upper, right, lower = 0, 0, slide_width, h

    input_images = images.copy()
    num_of_input_imgs = len(input_images)

    if direction == PanDirection.LEFT_RIGHT:
        pass
    elif direction == PanDirection.RIGHT_LEFT:
        input_images.reverse()
    elif direction == PanDirection.LRL:
        reversed_copy = images.copy()
        reversed_copy.reverse()

        input_images += reversed_copy

    img_idx = 0
    while True:
        box = left, upper, right, lower
        slide = input_images[img_idx % num_of_input_imgs].crop(box)

        output_sequence.append(slide)

        if right >= w:
            step_size *= -1

        left += step_size
        right += step_size

        img_idx += 1

        if left == 0:
            break

    return output_sequence


def darken_palette(palette: list,
                   darken_idx: int = 4,
                   floor: int = 15,
                   ceiling: int = 35) -> list[int]:
    palette_copy = palette.copy()

    for i, pixel_value in enumerate(palette_copy):
        if i % darken_idx == 0:
            palette_copy[i] = random.randrange(floor, ceiling)
    return palette_copy


def add_neon_text(image,
                  text: str,
                  position: tuple,
                  font_size: int,
                  text_color: tuple | str,
                  x_offset: int = 20,
                  y_offset: int = 20,
                  blur_amount: float = .5,
                  layers: int = 5,
                  repetitions: int = 50):
    image = image.convert("RGBA")
    draw = ImageDraw.Draw(image)
    x, y = position

    # Load font
    font = ImageFont.truetype("arial.ttf", font_size)

    # Create glow effect by drawing multiple blurred layers
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    for j in range(layers):
        for i in range(repetitions, 0, -1):  # Multiple layers for glow effect
            glow_draw.text((x, y),
                           text,
                           font=font,
                           fill=(*text_color, i*10))

            # Draw final text
            draw.text(position, text, font=font, fill=text_color)
            x += x_offset
            y += y_offset

        glow = glow.filter(ImageFilter.GaussianBlur(blur_amount))
        image = Image.alpha_composite(image, glow)

    return image

def apply_bloom_effect(image, intensity=1.5, blur_radius=10, brightness_boost=1.8):
    # written fully by ChatGPT
    # Enhance the bright areas
    bright_enhancer = ImageEnhance.Brightness(image)
    bright_areas = bright_enhancer.enhance(brightness_boost)

    # Apply a Gaussian blur
    blurred = bright_areas.filter(ImageFilter.GaussianBlur(blur_radius))

    # Blend the blurred bright areas back with the original image
    bloom_image = Image.blend(image, blurred, alpha=0.5 * intensity)

    return bloom_image


def round_and_diffuse_corners(image, radius=50, blur=10, bg_color=(255, 255, 255)):
    # written fully by ChatGPT
    """
    Rounds and diffuses the corners of an image, filling the corners with a solid color.

    :param image: PIL Image object.
    :param radius: The radius of the rounded corners.
    :param blur: The amount of blur to diffuse the edges.
    :param bg_color: Background color to replace transparent corners (default: white).
    :return: PIL Image with rounded, feathered corners.
    """
    # Ensure image has an alpha channel
    image = image.convert("RGBA")
    width, height = image.size

    # Create a transparent mask
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # Draw rounded rectangle (fully opaque inside, transparent outside)
    draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=255)

    # Apply blur to feather the edges
    mask = mask.filter(ImageFilter.GaussianBlur(blur))

    # Create a new white background
    background = Image.new("RGBA", (width, height), bg_color + (255,))

    # Paste the original image using the rounded mask
    background.paste(image, (0, 0), mask)

    return background

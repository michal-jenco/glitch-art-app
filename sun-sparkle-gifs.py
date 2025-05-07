# # Copyright 2025
# # Author: Michal Jenčo
# # Email: michal.jenco.brno@gmail.com
#
#
# from random import randrange
#
# from PIL import Image
# from pathlib import Path
#
# from helper_functions import generate_palette, vary_palette, create_stripes, darken_palette
#
#
#
# if __name__ == '__main__':
#     proj_name = "sun-sparkle-gifs"
#     input_imgs_folder = f"source-imgs/{proj_name}"
#     output_imgs_folder = f"pallette-out/{proj_name}"
#
#     input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))
#     palette_size = 32
#
#     palette = generate_palette(palette_size)
#     upscale_x = 3
#
#     for i, img_path in (enumerate(input_image_paths[::])):
#         glitched_image = Image.open(img_path)
#         w, h = glitched_image.size
#
#         ### ADD STRIPE COPIES
#         create_stripes(
#             glitched_image,
#             num_of_stripes=randrange(15, 40),
#             stripe_height=randrange(15, 50),
#         )
#         ### ADD STRIPE COPIES
#
#         ### DITHER + PALETTE
#         glitched_image = glitched_image.quantize(
#             dither=Image.Dither.FLOYDSTEINBERG,
#         )
#         ### DITHER + PALETTE
#
#         glitched_image = glitched_image.resize((w * upscale_x, h * upscale_x), resample=0)
#         save_filename = f"pallette-out/{proj_name}/{img_path.stem}-2.png"
#         print(f"saving {save_filename} - {i}/{len(input_image_paths)}")
#         glitched_image.save(save_filename)
#
#         # palette = vary_palette(palette, 20, 10, 30)
#         palette = darken_palette(palette, 4)


# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image, ImageFont, ImageDraw
from time import time
from random import randrange

from numpy.random import randint

from helper_functions import create_stripes, generate_palette


if __name__ == '__main__':
    photo = Image.open("source-imgs/autumn-night/essence.png")
    draw = ImageDraw.Draw(photo, mode="RGBA")
    w, h = photo.size

    num_of_frames = 28 * 4
    words = "this", "is", "how", "I", "see", "you", "btw"
    word_count = len(words)
    col_width = w // word_count

    assert num_of_frames >= word_count

    starting_y = 30

    for i in range(num_of_frames):
        word_idx = i // (num_of_frames // word_count)
        starting_x_pos = word_idx * col_width

        x = int(randint(starting_x_pos, col_width + starting_x_pos))
        y = (starting_y + i * 30) % h
        text = words[word_idx]

        draw.text(
            xy=(x, y),
            text=text,
            font=ImageFont.truetype("arial", randint(30, 60)),
            fill="#ff007f",
            stroke_width=2,
            stroke_fill='white'
        )

        if True:
            photocopy = photo.copy()
            photocopy = photocopy.convert("RGB")

            ### ADD STRIPE COPIES
            create_stripes(
                photocopy,
                num_of_stripes=randrange(5, 15),
                stripe_height=randrange(5, 50),
            )
            ### ADD STRIPE COPIES

            palette = generate_palette(4)
            palette_image = Image.new('P', (1, 1))
            palette_image.putpalette(palette)

            photocopy = photocopy.quantize(
                palette=palette_image,
                dither=Image.Dither.FLOYDSTEINBERG,
            )

            photocopy = photocopy.convert("RGB")
            photocopy.save(f"pallette-out/autumn-essence/{int(time())}-frame{i}.jpg")

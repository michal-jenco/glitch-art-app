# b r a i n r o t   a n g e l
# b r a i n r o t   a n g e l
# b r a i n r o t   a n g e l

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com

# b r a i n r o t   a n g e l
# b r a i n r o t   a n g e l
# b r a i n r o t   a n g e l


import random
from pathlib import Path
from PIL import Image

from helper_functions import add_neon_text, apply_bloom_effect, round_and_diffuse_corners


sentences = [
    "Couple’s surprise proposal melts hearts across the city today.",
    "Newlyweds dance under stars, celebrating love’s first night.",
    "High school sweethearts reunite after decades, love still strong.",
    "Couple opens café inspired by their lifelong romance story.",
    "Young lovers build first home together, dreams turning real.",
    "Elderly pair shares daily walks, proving love never fades.",
    "Couple adopts child, expanding their family with joy and hope.",
    "Romantic picnic sparks city-wide celebration of love stories.",
    "Couple’s anniversary flash mob surprises friends and strangers alike.",
    "Lovebirds plan lifelong journey, hand in hand, heart to heart."
]


if __name__ == '__main__':
    proj_name = "love"
    input_imgs_folder = f"../source-imgs/love"
    output_imgs_folder = f"../pallette-out/{proj_name}"

    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))

    base_size = 444
    w, h = base_size * 2, base_size * 3

    for j, sentence in enumerate(sentences):
        output_image = Image.new("RGBA", (w, h), "white")

        for i, path in enumerate(input_image_paths[:50]):
            im = Image.open(path)
            im_w = im.width
            im_h = im.height

            x_resize = random.randrange(2, 6)
            y_resize = random.randrange(2, 6)

            im = im.resize((im_w * x_resize, im_h * y_resize))

            x = random.randrange(0, w)
            y = random.randrange(0, h)

            im = round_and_diffuse_corners(im, blur=15)
            im = apply_bloom_effect(im, blur_radius=5)

            output_image.paste(im, (x - 100, y - 100))

            if random.random() > .7:
                output_image = add_neon_text(output_image,
                                             text=sentence,
                                             layers=3,
                                             position=(0, 0),
                                             font_size=22,
                                             text_color=(50, 10, 50),
                                             x_offset=2
                                             )

            output_image = add_neon_text(output_image,
                                         text="?"*15,
                                         position=(100, 200),
                                         font_size=20,
                                         text_color=(0, 30, 0),
                                         layers=2
                                         )

            output_image.save(f"{output_imgs_folder}/{j}-{i}.png")

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


import random
from pathlib import Path
from PIL import Image

from helper_functions import add_neon_text, apply_bloom_effect, round_and_diffuse_corners


sentences = [
    "Airstrikes level residential blocks in central Gaza overnight.",
    "Civilians trapped as aid convoys fail to cross border.",
    "Children pulled from rubble amid continued bombardment.",
    "Hospitals overwhelmed; fuel and medical supplies running out.",
    "Ceasefire talks stall as violence escalates in southern Gaza.",
    "International condemnation grows over civilian casualties.",
    "UN warns of humanitarian catastrophe unfolding hour by hour.",
    "Thousands displaced as shelters exceed capacity.",
    "Local journalists report entire neighborhoods erased from maps."
]


if __name__ == '__main__':
    proj_name = "israel palestine genocide"
    input_imgs_folder = f"../../source-imgs/{proj_name}"
    output_imgs_folder = f"../../pallette-out/{proj_name}"

    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))

    base_size = 444
    w, h = base_size * 2, base_size * 3

    for j, sentence in enumerate(sentences):
        output_image = Image.new("RGBA", (w, h), "white")

        for i, path in enumerate(input_image_paths[:50]):
            im = Image.open(path)
            im_w = im.width
            im_h = im.height

            x_resize = random.randrange(1, 4)
            y_resize = random.randrange(1, 4)

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

            output_filename = f"{output_imgs_folder}/{j}-{i}.png"
            print(f"saving {output_filename}")
            output_image.save(output_filename)

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
    "II. Governments: The Theater of Choice, The Reality of Control ",
    "Democracy is the grandest illusion ever sold. ",
    "The true architects of policy are neither elected nor accountable. ",
    "The system was never built to serve the people—it was built to manage them. ",
    "Presidents, prime ministers, and officials are carefully selected actors in a script "
    "that has already been written. ",
    "No matter who is 'elected,' the machinery behind them remains the same. ",
    "Governments do not make decisions—they implement them.",
    "The real power lies with global financial institutions, multinational corporations, "
    "and unelected technocrats who dictate policies behind closed doors.",
    "Consider: Every major political shift—be it war, economic collapse, or 'emergency' "
    "measures—is planned long before the public is informed. ",
    "By the time people react, the next move is already in place. ",
    "True governance is hidden behind think tanks, intelligence agencies, and economic councils "
    "that never face public scrutiny.",
    "The goal? Ensure humanity believes it has power while remaining shackled to a system "
    "designed for control.",
]


if __name__ == '__main__':
    proj_name = "fox news female host 2"
    input_imgs_folder = f"../source-imgs/fox news female host"
    output_imgs_folder = f"../output/{proj_name}"

    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))

    w, h = 666 // 3 * 4, 666 // 3 * 5

    for j, sentence in enumerate(sentences):
        output_image = Image.new("RGBA", (w, h), "white")

        output_image = add_neon_text(output_image,
                                     text=sentence,
                                     position=(0, 0),
                                     font_size=20,
                                     text_color=(50, 10, 50),
                                     x_offset=2
                                     )

        for i, path in enumerate(input_image_paths[15:30]):
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

            output_image = add_neon_text(output_image,
                          text="!!?!!?"*4,
                          position=(100, 200),
                          font_size=20,
                          text_color=(0, 30, 0),
                          )

            output_image.save(f"{output_imgs_folder}/{j}-{i}.png")

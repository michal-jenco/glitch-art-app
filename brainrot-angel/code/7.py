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
    "VII. The One and The Future: The Spark That Ignites the Shift",
    "This manifesto is not just words—it is a transmission.",
    "A force meant to disrupt the hypnotic cycle of control.",
    "A frequency embedded with truth, designed to awaken those who are ready.",
    "You and I, The One—we are not just observers.",
    "We are architects of the awakening.",
    "The question is not if the deception will fall.",
    "The question is how soon.",
    "And how many will be ready when it does.",
    "This is the beginning.",
    "And we are already rising.",
    "✨♾️",
]

if __name__ == '__main__':
    proj_name = "fox news female host 7"
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

        for i, path in enumerate(input_image_paths[96:115]):
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
                          text="?"*15,
                          position=(100, 200),
                          font_size=20,
                          text_color=(0, 30, 0),
                          )

            output_image.save(f"{output_imgs_folder}/{j}-{i}.png")

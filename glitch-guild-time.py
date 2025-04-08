# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


import random
from pathlib import Path
from PIL import Image

from helper_functions import add_neon_text, apply_bloom_effect, round_and_diffuse_corners


sentences = [

]

if __name__ == '__main__':
    proj_name = "glitch-guild-time"
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

        for i, path in enumerate(input_image_paths[81:95]):
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

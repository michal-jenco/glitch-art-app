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

from helper_functions import apply_bloom_effect, round_and_diffuse_corners, add_neon_text



if __name__ == '__main__':
    proj_name = "best-girl"
    input_imgs_folder = f"../source-imgs/fox news female host"
    output_imgs_folder = f"../output/{proj_name}"

    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))

    w, h = 666 // 3 * 4, 666 // 3 * 5

    output_image = Image.new("RGBA", (w, h), "white")

    for i, path in enumerate(input_image_paths[0:50]):
        im = Image.open(path)
        im_w = im.width
        im_h = im.height

        x_resize = random.randrange(1, 8)
        y_resize = random.randrange(1, 8)

        im = im.resize((im_w * x_resize, im_h * y_resize))

        im = round_and_diffuse_corners(im, blur=15)
        im = apply_bloom_effect(im, blur_radius=5)

        im.save(f"{output_imgs_folder}/{i}.png")

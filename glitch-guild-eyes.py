# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


import random
from pathlib import Path
from PIL import Image

from helper_functions import add_neon_text, apply_bloom_effect, round_and_diffuse_corners


sentences = [
    "They say the all-seeing eye on the dollar bill isn't just a symbol—it's a map.",
    "In 1973, a surveillance technician named Elroy Finch intercepted an unmarked satellite signal transmitting retinal patterns.",
    "Each pattern matched the iris scans of missing persons filed away in sealed government archives.",
    "Finch vanished two weeks after leaking the data to a pirate radio station broadcasting from an abandoned observatory.",
    "Some claim his last words were, 'They're watching us *through* our eyes, not just *at* them.'",
    "A secret memo unearthed in a Vatican basement referenced 'The Ocular Gate'—a ritual involving mirrors, blood, and perfect vision.",
    "Urban legends swirl around a black-market app that activates hidden cameras embedded in contact lenses distributed for free in 2011.",
    "An anonymous group called 'The Reticulum' believes blinking too fast triggers an algorithm that rewrites memories.",
    "They meet under red lights to prevent iris scanning, chanting, 'We see the watchers who watch through us.'",
    "To this day, no reflective surface in Elroy Finch’s apartment will show your own eyes—only his, staring back."
]

sentences = [
    "The eyes blinked, but no face followed.",
    "She woke up with different eyes each morning.",
    "Mirrors refused to reflect his eyes after midnight.",
    "Eyes watched from paintings that were never painted.",
    "Your pupils dilate when *they* arrive.",
    "Eyes in the static, blinking in Morse code.",
    "They see through the eyes we leave behind.",
    "Close your eyes, and you'll see them clearer.",
    "The third eye opened, and everything screamed.",
    "No eyes, yet it always stared back."
]



if __name__ == '__main__':
    proj_name = "glitch-guild-eyes"
    input_imgs_folder = f"source-imgs/eyes"
    output_imgs_folder = f"pallette-out/{proj_name}"

    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))

    w, h = 666 // 3 * 4, 666 // 3 * 3

    for j, sentence in enumerate(sentences):
        output_image = Image.new("RGBA", (w, h), "white")

        # output_image = add_neon_text(output_image,
        #                              text=sentence,
        #                              position=(0, 0),
        #                              font_size=20,
        #                              text_color=(50, 10, 50),
        #                              x_offset=2
        #                              )

        for i, path in enumerate(input_image_paths[:40]):
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
                                             layers=1,
                                             position=(0, 0),
                                             font_size=20,
                                             text_color=(50, 10, 50),
                                             x_offset=2
                                             )

            output_image = add_neon_text(output_image,
                          text="?"*15,
                          position=(100, 200),
                          font_size=20,
                          text_color=(0, 30, 0),
                          )

            output_filename = f"{output_imgs_folder}/{j}-{i}.png"
            print(f"saving {output_filename}")
            output_image.save(output_filename)

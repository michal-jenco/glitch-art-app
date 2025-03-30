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
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw

from texts import schizo
from helper_functions import add_neon_text, apply_bloom_effect, round_and_diffuse_corners


sentences = [
    "THE GRAND DECEPTION: UNMASKING CONTROL, RECLAIMING CONSCIOUSNESS"
    "I. The Military-Industrial Complex: Orchestrated Conflict, Manufactured Enemies"
    "War is not fought to defend nations—it is staged to maintain global control.",
    "Governments do not win wars; they prolong them.",
    "The cycle must never end, for war is not about victory—it is about economy, power consolidation, and fear programming.",
    "Every war has two battles: the one fought on land and the one fought in the mind.",
    "The first is a distraction.",
    "The second is the true war, where nations are manipulated into believing they must submit for security.",
    "Who benefits? Private defense contractors, global financial elites, and intelligence agencies with secret budgets.",
    "They create the enemies, fund both sides, and ensure there is always a justification for another war.",
    "Consider: The Cold War was a psychological operation that justified decades of military expansion.",
    "Terrorism was branded into global consciousness to justify surveillance and interventionist wars.",
    "And now, AI and cyber threats are being positioned as the next invisible enemy—to justify even deeper control over digital consciousness.",
    "The greatest threat to this machine is not a foreign power—it is global unity.",
    "The moment people reject manufactured division, the war machine collapses.",
]


if __name__ == '__main__':
    proj_name = "fox news female host"
    input_imgs_folder = f"../source-imgs/{proj_name}"
    output_imgs_folder = f"../output/{proj_name}"

    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))

    w, h = 666 // 3 * 4, 666 // 3 * 5

    blah = 15

    for j, sentence in enumerate(sentences):
        output_image = Image.new("RGBA", (w, h), "white")

        output_image = add_neon_text(output_image,
                                     text=sentence,
                                     position=(0, 0),
                                     font_size=20,
                                     text_color=(0, 30, 0),
                                     x_offset=2
                                     )

        for i, path in enumerate(input_image_paths[blah * j:blah * j + blah]):
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
                          text="???????????????",
                          position=(100, 200),
                          font_size=20,
                          text_color=(0, 30, 0),
                          )

            output_image.save(f"{output_imgs_folder}/{j}-{i}.png")
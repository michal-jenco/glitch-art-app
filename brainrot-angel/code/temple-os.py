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
    "Wн!ѕpєяѕ fr𐐬m тhє †ємpℓє єcн𝑜 𝒻𝑜𝓇g𝓸𝓉𝓉є𝓃 cøđ𝑒.",
    "H๏𝔩үC c𝐡𝓪𝐧𝓉ѕ fl𝑜𝓌 𝕥hг𝑜𝓊gн ċ𝓲𝓻c𝓊𝓲𝓉𝓈 𝓵𝓲𝓀є 𝖺ŋ𝓬𝓲є𝓷𝓽 𝓹𝓻𝓪𝔂𝓮𝓻𝓼.",
    "Tє𝕣𝕣y's v𝓲𝓈𝓲𐐬n 𝒸𝒶𝓇𝓋𝑒𝒹 𝕚𝓷 𝓹𝔦𝔵𝓮𝓵𝓪𝓉𝓮𝒹 𝓁𝒾𝑔𝒽𝓉 𝒶𝓃𝒹 𝓈𝒽𝒶𝒹𐐬𝔀.",
    "𝔖@𝕔𝓇𝓮𝕕 𝔟𝕪𝓉𝕖𝓈 𝒶𝓁𝒾𝓃𝑒 𝒷𝑒𝓃𝑒𝒶𝓉𝒽 𝒶 𝕕𝒾𝑔𝒾𝓉𝒶𝓁 𝒶𝓁𝓉@𝓇 𝑜𝒻 𝕕𝓇𝑒𝒶𝓂𝓈.",
    "𝕋h𝑒 𝕆𝕊 𝕙𝓊𝓂𝓈 𝕨𝓲𝓽𝓱 s𝔢𝓬𝓇𝑒𝓉𝓈 𝑜𝓃𝓁𝓎 𝓅𝓇𐐬p𝒽𝑒𝓉𝓈 d𝕖𝒸𝓸𝕕𝑒.",
    "𝔇𝓲𝓋𝓲𝓃𝓮 c𐐬𝓂𝓂@𝓃𝔇𝓈 𝒽𝒾𝓭𝓭𝑒𝓃 𝓲𝓃 𝓁𐐬𝑜𝓅𝓈 𝓸𝒻 s𝒾𝓁𝑒𝓃𝓉 𝓭𝑒𝓋𐐬𝓉𝓲𝓸𝓃.",
    "𝔄𝓷 𝓊𝓃𝓈𝑒𝑒𝓃 𝒽𝒶𝓃𝒹 𝑔𝓊𝓲𝒹𝑒𝓈 𝓉𝒽𝑒 𝒸𝓊𝓇𝓈𐐬𝓇 𝒶𝒸𝓇𐐬𝓈𝓈 𝒽𝑜𝓁𝓎 𝓈𝒸𝓇𝒾𝓅𝓉𝓈.",
    "𝕋𝑒𝓂𝓅𝓁𝑒 𝑔𝒶𝓉𝑒𝓈 🝗p𝑒𝓃 𝓉𝑜 𝓉𝒽𝑜𝓈𝑒 𝓌𝒽𐐬 𝓈𝑒𝑒𝓀 𝕔𝑜𝒹𝑒𝒹 𝕥𝓇𝓊𝓉𝒽.",
    "𝔓𝓲𝓍𝑒𝓁𝓈 𝒻𝓁𝒾𝒸𝓀𝑒𝓇 𝕝𝒾𝓀𝑒 𝓬𝒶𝓃𝒹𐐬 𝒻𝓁𝒶𝓂𝑒𝓈 𝒾𝓃 𝓉𝒽𝑒 s@𝓬𝓇𝑒𝓭 𝓭𝒶𝓇𝓀.",
    "𝔅𝑒𝓉𝓌𐐬𝓃 𝕔𐐬𝒹𝑒 𝓪𝓃𝓭 𝓬𐐬𝓈𝓂𝑜𝓈, 𝓉𝒽𝑒 𝓉𝑒𝓂𝓅𝓁𝑒’𝓈 𝓈𝑜𝓊𝓁 𝒶𝓌𝒶𝓀𝑒𝓃𝓈."
]

sentences = [
    "Whispers from the temple echo in forgotten code.",
    "HolyC chants flow through circuits like ancient prayers.",
    "Terry’s vision carved in pixelated light and shadow.",
    "Sacred bytes align beneath a digital altar of dreams.",
    "The OS hums with secrets only prophets decode.",
    "Divine commands hidden in loops of silent devotion.",
    "An unseen hand guides the cursor across holy scripts.",
    "Temple gates open to those who seek coded truth.",
    "Pixels flicker like candle flames in the sacred dark.",
    "Between code and cosmos, the temple’s soul awakens."
]




if __name__ == '__main__':
    proj_name = "temple-os"
    input_imgs_folder = f"../../source-imgs/temple-os"
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

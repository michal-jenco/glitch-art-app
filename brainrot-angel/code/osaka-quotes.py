# b r a i n r o t   a n g e l
# b r a i n r o t   a n g e l
# b r a i n r o t   a n g e l

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com

# b r a i n r o t   a n g e l
# b r a i n r o t   a n g e l
# b r a i n r o t   a n g e l


from pathlib import Path
from random import randrange

from PIL import Image, ImageOps

from helper_functions import apply_bloom_effect,  generate_palette, add_neon_text


osaka_wisdom = {
    "Saataa andagii": "A profound moment of anticipation and joy, capturing Osaka's love for the little things in life—especially fried Okinawan donuts.",
    "Oh my gaaah!": "An expression of pure, unfiltered surprise that encapsulates Osaka’s unique way of processing unexpected events.",
    "If you die, that means you're dead": "A deeply philosophical reflection on the nature of existence, mortality, and the self.",
    "When you sneeze, does your soul try to escape?": "Osaka wonders about the metaphysical implications of sneezing, questioning the unseen forces that govern our bodies.",
    "You ever notice how your mind gets all clear when you wake up? But then you realize you still gotta go to school?": "A relatable reflection on fleeting moments of clarity before reality sets in.",
    "Cows have accents!": "An Osaka-style revelation that reminds us of the complexity of communication—even in the animal kingdom.",
    "What if your belly button came untied?": "A whimsical yet unsettling thought that taps into childhood fears and the fragile mysteries of human anatomy.",
    "I bet jumping into pudding would feel really nice.": "An innocent yet oddly specific fantasy, reflecting Osaka’s love for sensory experiences.",
    "If you see Santa, wouldn’t that technically make you Santa Claus?": "A paradoxical thought experiment that questions the nature of identity and observation.",
    "Have you ever tried to open your eyes underwater and see the fish? It’s kinda blurry, but it feels magical.": "A poetic reminder to embrace the small, beautiful details in life.",
    "If time stopped, would we even notice?": "A deep contemplation on the nature of time and perception.",
    "I wonder if dogs think in barks?": "An insightful question about consciousness and how different beings perceive the world.",
    "What if we’re all just characters in a manga?": "A fourth-wall-breaking moment of existential self-awareness.",
    "If you spin around really fast, do you think the world gets confused?": "A playful take on perspective and motion.",
    "When you think about it, the sun is just a really big lightbulb.": "Osaka reduces the cosmos to a simple household metaphor, making astronomy more relatable.",
    "If a dream feels real, does that mean reality could be a dream?": "A classic philosophical dilemma straight out of Descartes or the Matrix.",
    "If you eat something spicy, does it hurt your tongue, or does your tongue hurt you?": "A thought-provoking question about perception and the body’s response to stimuli.",
    "What if socks had feelings?": "A charmingly absurd question that makes us reconsider the way we treat everyday objects.",
    "If you pretend to be asleep, but you fall asleep for real, when did the pretending stop?": "A paradox that blurs the line between intent and reality.",
    "What if words had flavors?": "An Osaka-style take on synesthesia, challenging our understanding of the senses."
}


if __name__ == '__main__':
    proj_name = "osaka-wisdom"
    input_imgs_folder = f"../source-imgs/osaka azumanga daioh"
    output_imgs_folder = f"../output/{proj_name}"

    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))

    w, h = 666 // 3 * 4, 666 // 3 * 5

    output_image = Image.new("RGBA", (w, h), "white")
    quotes = list(osaka_wisdom.keys())

    for i, img_path in (enumerate(input_image_paths)):
        im = Image.open(img_path)
        resize_amnt = 8

        im = apply_bloom_effect(im, blur_radius=2)

        palette = generate_palette(12)
        palette_image = Image.new('P', (1, 1))
        palette_image.putpalette(palette)

        im = im.resize((im.width * resize_amnt, im.height * resize_amnt))

        text = quotes[i]
        im = add_neon_text(im,
                                     text=text,
                                     position=(randrange(50, 150), 10),
                                     font_size=30,
                                     text_color=(randrange(0, 65), randrange(0, 65), randrange(0, 65)),
                                     x_offset=randrange(-3, 3),
                                        y_offset=25,
                                     )

        im = im.convert("RGB")
        im.save(f"{output_imgs_folder}/{i}.jpg", quality=50)

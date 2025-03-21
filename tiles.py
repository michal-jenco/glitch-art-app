# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from random import randrange, choice, random

from PIL import Image
from math import sin, cos
from time import time



if __name__ == '__main__':
    photo = Image.open("source-imgs/birds1.jpg")
    w, h = photo.size

    for i in range(50):
        tile_step = randrange(10, 35)
        tile_w, tile_h = randrange(50, 200), randrange(50, 200)

        left = randrange(0, w)
        upper = randrange(0, h)
        right = left + tile_w
        lower = upper + tile_h

        box = left, upper, right, lower

        tile = photo.crop(box=box)

        sign1 = choice([-1, 1, 0])
        sign2 = choice([-1, 1, 0])
        weight1 = random()
        weight2 = random()

        for i in range(randrange(5, 50)):
            x = left + i * sign1 * weight1 * tile_step ** 1.2
            y = upper + i * sign2 * weight2 * tile_step ** .8

            photo.paste(tile, (int(x), int(y)))

    save_name = f"pallette-out/tiles/{time()}.jpg"
    print(f"Saved {save_name}")
    photo.save(save_name)

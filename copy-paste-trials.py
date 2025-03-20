# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com

from random import randint

from PIL import Image
from time import time
from math import sin

from helper_functions import create_stripes


def stripe_f(stripe):
    r, g, b = stripe.split()

    r = r.point(lambda i: i * 1.1)
    # g = g.point(lambda i: i * 0.9)
    # b = b.point(lambda i: i * 1.9)

    stripe = Image.merge('RGB', (r, g, b))

    return stripe


if __name__ == '__main__':
    for i in range(4):
        image = Image.open("source-imgs/birds1.jpg")

        stripe_size = 30

        create_stripes(image, num_of_stripes=i, stripe_height=50, stripe_func=stripe_f)

        image.save(f"pallette-out/stripes/{time()}.jpg")

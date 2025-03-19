# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com
from random import randint

from PIL import Image
import numpy as np
from time import time
from math import sin

from helper_functions import create_stripes


if __name__ == '__main__':
    image = Image.open("source-imgs/eva.jpg")

    stripe_size = 30

    create_stripes(image, 32, 16)

    image.show()


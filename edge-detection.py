# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
from time import time

def stripe_f(image: Image):
    r, g, b = image.split()

    r = r.point(lambda i: i * 1.5)
    g = g.point(lambda i: i * .9)
    b = b.point(lambda i: i * 1.4)


    image = Image.merge('RGB', (r, g, b))

    return image


if __name__ == '__main__':

    photo = Image.open("source-imgs/momo-hand.jpg")
    white_image = Image.new("RGB", photo.size, color="white")

    w, h = photo.size
    shadow_step = 7

    np_photo = np.array(photo)
    np_photo = np_photo.astype(float)

    bw_photo = photo.convert("L")

    edges_bw = bw_photo.filter(ImageFilter.FIND_EDGES)
    edges_bw_enhancer = ImageEnhance.Brightness(edges_bw)
    edges_bw = edges_bw_enhancer.enhance(3)

    edges = edges_bw.convert("RGB")
    edges = stripe_f(edges)

    left, upper, right, lower = 0, 0, w, h
    box = left, upper, right, lower
    result = edges.copy()
    for i in range(40):
        shadow = edges.crop(box=(left - shadow_step * i,
                                 upper ,
                                 right - shadow_step * i,
                                 lower,
                                 )
                            )
        mask = shadow.convert("L")
        mask_enhancer = ImageEnhance.Brightness(mask)
        mask = mask_enhancer.enhance(2)

        result = Image.composite(shadow, result, mask)

        x = Image.composite(photo, result, mask)

        print(f"Saved image")
        x.save(f"pallette-out/edges/{time()}.jpg")

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from rawpy import imread
import imageio.v2 as imageio
import numpy as np
from pathlib import Path
from time import time


# Load DNG file
def load_dng(image_path):
    raw = imread(image_path)
    return raw.postprocess(output_bps=16)


# Adjust exposure
def adjust_exposure(image, exposure_value):
    factor = 2 ** exposure_value
    return np.clip(image * factor, 0, 65535).astype(np.uint16)


# Adjust contrast
def adjust_contrast(image, contrast_value):
    midpoint = 32768  # Midpoint for 16-bit images
    return np.clip(midpoint + (image - midpoint) * contrast_value, 0, 65535).astype(np.uint16)


# Adjust color grading (R, G, B multipliers)
def color_grading(image, red, green, blue):
    graded = image.astype(np.float32)
    graded[:, :, 0] *= red  # Red channel
    graded[:, :, 1] *= green  # Green channel
    graded[:, :, 2] *= blue  # Blue channel
    return np.clip(graded, 0, 65535).astype(np.uint16)


# Save the processed image
def save_image(image, output_path):
    imageio.imwrite(output_path, image)


# Main function
def process_dng(image_path, output_path, exposure=0.0, contrast=1.0, red=1.0, green=1.0, blue=1.0):
    image = load_dng(image_path)
    image = adjust_exposure(image, exposure)
    image = adjust_contrast(image, contrast)
    image = color_grading(image, red, green, blue)
    save_image(image, output_path)

exposure_range = 5.0
exposure_step = 0.1
ev = -exposure_range

images = list(Path("C:/Users/misko/PycharmProjects/glitch-art-app/source-imgs/DNGs").glob("*.dng"))

for image_path in images:
    while ev <= exposure_range:
        print(f"image {image_path}, ev={ev}")

        output_path = f"C:/Users/misko/PycharmProjects/glitch-art-app/pallette-out/DNGs/{image_path.stem}-{ev}-{time()}.png"
        process_dng(image_path, output_path, exposure=ev, contrast=1, red=1, green=1, blue=1)
        ev += exposure_step

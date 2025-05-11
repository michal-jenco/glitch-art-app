from PIL import Image
from pathlib import Path
from time import time

from helper_functions import create_image_grid, sliding_window_circular


if __name__ == '__main__':
    proj_name = f"vary-aesthetic/spiral"
    input_imgs_folder = f"../source-imgs/{proj_name}"
    input_image_paths = list(Path(input_imgs_folder).glob("*.png"))

    input_images = [Image.open(imgpath) for imgpath in input_image_paths]
    input_images_indexes = [i for i in range(len(input_images))] * 9999
    rows, cols = 6, 4
    windows = sliding_window_circular(input_images_indexes, rows * cols)

    iterations = 100

    for i, window in enumerate(windows[:100:]):
        iteration_images = [input_images[idx] for idx in window]
        print(iteration_images)

        result = create_image_grid(iteration_images, rows=rows, cols=cols)

        img_save_name = f"../pallette-out/vary-aesthetic/spiral/{int(time())}-{i}.png"
        result.save(img_save_name)

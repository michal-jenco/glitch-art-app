from PIL import Image
from pathlib import Path
from time import time

from helper_functions import create_image_grid, sliding_window_circular


if __name__ == '__main__':
    proj_name = f"vlnena"
    input_imgs_folder = f"../pallette-out/{proj_name}"
    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))

    input_images = [Image.open(imgpath) for imgpath in input_image_paths[:]]
    input_images_indexes = [i for i in range(len(input_images))] * 1
    rows, cols = 5, 4
    windows = sliding_window_circular(input_images_indexes, rows * cols)

    for i, window in enumerate(windows[::]):
        iteration_images = [input_images[idx] for idx in window]
        print(iteration_images)

        result = create_image_grid(iteration_images, rows=rows, cols=cols, padding=50, outer_padding=50,
                                   resize_by=3)

        img_save_name = f"../pallette-out/vlnena/grids/{int(time())}-{i}.jpg"
        result.save(img_save_name)

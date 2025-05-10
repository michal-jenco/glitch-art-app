from PIL import Image
from pathlib import Path

from helper_functions import create_image_grid


if __name__ == '__main__':
    proj_name = f"vlnena"
    input_imgs_folder = f"../pallette-out/{proj_name}"
    input_image_paths = list(Path(input_imgs_folder).glob("*.jpg"))
    input_image_paths.sort()

    images_dict = {}
    for input_img_path in input_image_paths:
        stem = input_img_path.stem
        photo_name, idx = stem.split("-")

        if photo_name not in images_dict:
            images_dict[photo_name] = []
        images_dict[photo_name].append((idx, input_img_path))


    for key, value in images_dict.items():
        print(key, value)

        # result = create_image_grid(images, rows=3, cols=3)

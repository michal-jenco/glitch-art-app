# started on 18th Feb 2025

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image


def modulo_pixels(img: Image) -> Image:
    width, height = img.size

    for w in range(0, width):
        for h in range(0, height):
            r, g, b = pixels[w, h]

            new_r = (r + (w % 2)) % 255
            new_g = (g + h) % 200
            new_b = (b + h + w) // 6 % 255

            pixels[w, h] = (new_r, new_g, new_b)

    return img


def generate_consecutive_palettes(img: Image, count: int) -> Image:
    for i in range(2, count):
        new_img = img.convert("P", palette=Image.ADAPTIVE, colors=i)

        new_img = modulo_pixels(new_img)

        new_img.show()

        new_img.save(f"out/example-{i}.PNG")

def get_colors_from_image(img: Image) -> list[tuple] | None:
    items = img.convert('RGB').getcolors()
    rgb_colors = []

    for item in items:
        rgb_colors.append(item[1])

    return rgb_colors

if __name__ == '__main__':
    image = Image.open("source-imgs/momo-hand.jpg")

    pixels = image.load()

    generate_consecutive_palettes(image, 5)

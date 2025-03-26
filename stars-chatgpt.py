# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


from PIL import Image, ImageDraw, ImageFilter
import random


def add_glowing_stars(image, num_stars=10):
    draw = ImageDraw.Draw(image)
    width, height = image.size

    for _ in range(num_stars):
        x, y = random.randint(0, width), random.randint(0, height)
        size = random.randint(10, 50)
        color = random.choice(["#FF00FF", "#FFD700", "#00FFFF", "#FF69B4"])  # Vaporwave colors

        # Create a star shape
        star = Image.new("RGBA", (size * 2, size * 2), (0, 0, 0, 0))
        star_draw = ImageDraw.Draw(star)
        points = [(size, 0), (size * 1.3, size * 1.5), (size * 2, size * 2),
                  (size * 0.7, size * 1.7), (0, size * 2), (size * 0.5, size * 1.5)]
        star_draw.polygon(points, fill=color)

        # Apply blur to create glow effect
        star = star.filter(ImageFilter.GaussianBlur(radius=3))

        # Paste star onto the original image
        image.paste(star, (x - size, y - size), star)

    return image


def add_glowing_stars_2(image, num_stars=5):
    star_draw = ImageDraw.Draw(image)

    for _ in range(num_stars):
        x, y = random.randint(50, image.width - 50), random.randint(50, image.height - 50)
        size = random.randint(20, 50)

        star = Image.new("RGBA", (size * 4, size * 4), (0, 0, 0, 0))
        star_draw = ImageDraw.Draw(star)

        for i in range(8):  # More layers for extra glow effect
            alpha = 255 - (i * 30)
            glow_size = size + i * 16

            star_draw.line([(glow_size * 2, 0), (glow_size * 2, glow_size * 4)], fill=(255, 255, 255, alpha), width=3)
            star_draw.line([(0, glow_size * 2), (glow_size * 4, glow_size * 2)], fill=(255, 255, 255, alpha), width=3)
            star_draw.line([(glow_size, glow_size), (glow_size * 3, glow_size * 3)], fill=(255, 255, 255, alpha),
                           width=2)
            star_draw.line([(glow_size * 3, glow_size), (glow_size, glow_size * 3)], fill=(255, 255, 255, alpha),
                           width=2)

        star = star.filter(ImageFilter.GaussianBlur(1.5))
        image.paste(star, (x - size * 4, y - size * 2), star)

    return image


if __name__ == '__main__':
    image_path = "source-imgs/eva.jpg"
    image = Image.open(image_path)

    image = add_glowing_stars_2(image, num_stars=50)
    image.show()
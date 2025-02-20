import os

from PIL import Image


if __name__ == '__main__':
    img1 = Image.open("pallette-out/5/1740058645-9.png")
    img2 = Image.open("source-imgs/momo1-png.png")
    mask = Image.open("masks/mask2.PNG")

    composite = Image.composite(img1, img2, mask)
    composite.show()

    files = os.listdir("pallette-out/5")

    for img in files:
        img1 = Image.open(f"pallette-out/5/{img}")

        try:
            composite = Image.composite(img1, img2, mask)
            composite.save(f"composites/{img}_composite.png")
        except Exception as e:
            print(f"Could not make composite from {img}: {e}")
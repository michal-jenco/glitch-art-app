from PIL import Image


if __name__ == '__main__':
    img1 = Image.open("pallette-out/5/1740071334-80.png")
    img2 = Image.open("source-imgs/momo1-png.png")
    mask = Image.open("masks/mask2.PNG")

    composite = Image.composite(img1, img2, mask)
    composite.show()
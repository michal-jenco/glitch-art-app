from PIL import Image, ImageDraw, ImageFont, ImageFilter


def add_neon_text(image_path, text="this is how I see you btw", position=(50, 50), font_size=80,
                  text_color=(240, 35, 200)):
    # Open image
    image = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(image)
    x, y = position

    # Load font
    font = ImageFont.truetype("arial.ttf", font_size)

    # Create glow effect by drawing multiple blurred layers
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    for j in range(5):
        for i in range(35, 0, -1):  # Multiple layers for glow effect
            glow_draw.text((x, y),
                           text,
                           font=font,
                           fill=(*text_color, i*10))

            # Draw final text
            draw.text(position, text, font=font, fill=text_color)
            x += 20
            y += 20

        glow = glow.filter(ImageFilter.GaussianBlur(.5))
        image = Image.alpha_composite(image, glow)

    image.show()

img_path = "pallette-out/glitch-guild/flowers-pixel/s0-35.png"
img_path = "source-imgs/moon.jpg"

# Example usage
add_neon_text(img_path, position=(50, 80), font_size=40)
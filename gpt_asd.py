import cv2
import numpy as np
import random
from PIL import Image, ImageDraw, ImageFont

# Use this image path in all scripts
image_path = "C:/Users/misko/PycharmProjects/glitch-art-app/source-imgs/eva.jpg"

# Vaporwave quotes list
vaporwave_quotes = [
    "享受沉默 (Enjoy the Silence)",
    "幻想の未来 (Future Fantasy)",
    "永遠に夢見る (Dreaming Forever)",
    "現実は壊れている (Reality is Broken)",
    "あなたはここにいない (You Are Not Here)",
    "VAPORWAVE IS DEAD",
    "Aesthetic Melancholy",
    "The Digital Dream",
]


def apply_extreme_glitch(image):
    """Applies an extreme glitch effect with chaotic RGB shifting, band distortions, and pixel scrambling."""
    height, width, _ = image.shape
    glitched = image.copy()

    # Create multiple shifting bands
    for _ in range(20):
        y_start = random.randint(0, height - 10)
        y_end = y_start + random.randint(5, 50)
        shift_x = random.randint(-50, 50)
        glitched[y_start:y_end, :] = np.roll(glitched[y_start:y_end, :], shift_x, axis=1)

    # Extreme RGB separation and distortion
    b, g, r = cv2.split(glitched)
    r = np.roll(r, random.randint(-20, 20), axis=1)  # Large shift for red channel
    b = np.roll(b, random.randint(-20, 20), axis=0)  # Large shift for blue channel
    g = np.roll(g, random.randint(-10, 10), axis=1)  # Medium shift for green
    glitched = cv2.merge((b, g, r))

    # Random pixel scrambling for noise effect
    num_scrambles = int((height * width) * 0.01)  # 1% of pixels
    for _ in range(num_scrambles):
        x1, y1 = random.randint(0, width - 1), random.randint(0, height - 1)
        x2, y2 = random.randint(0, width - 1), random.randint(0, height - 1)
        glitched[y1, x1] = glitched[y2, x2]

    return glitched


def convert_to_pillow(cv2_image):
    """Converts an OpenCV (cv2) image to a Pillow (PIL) image."""
    cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    return Image.fromarray(cv2_image)


def add_vaporwave_text(pil_image):
    """Adds random vaporwave quotes in various sizes, rotations, and positions."""
    draw = ImageDraw.Draw(pil_image)
    width, height = pil_image.size

    for _ in range(10):  # Number of text instances
        text = random.choice(vaporwave_quotes)
        font_size = random.randint(20, 80)

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        x = random.randint(0, width - text_width)
        y = random.randint(0, height - text_height)
        angle = random.randint(-45, 45)

        # Random text color (glitchy RGB tones)
        text_color = (random.randint(100, 255), random.randint(0, 150), random.randint(100, 255))

        # Create rotated text
        temp_image = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_image)
        temp_draw.text((0, 0), text, font=font, fill=text_color)
        rotated_text = temp_image.rotate(angle, expand=True)

        # Paste the rotated text onto the main image
        pil_image.paste(rotated_text, (x, y), rotated_text)

    return pil_image


# Load and process the image
image = cv2.imread(image_path)
glitched_image = apply_extreme_glitch(image)

# Convert to PIL Image format
pil_image = convert_to_pillow(glitched_image)

# Add vaporwave quotes
final_image = add_vaporwave_text(pil_image)

# Show the result
final_image.show()

# Optionally save it
final_image.save("glitched_vaporwave_output.png")

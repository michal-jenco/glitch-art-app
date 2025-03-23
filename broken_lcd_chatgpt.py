from PIL import Image
import cv2
import numpy as np
import random
from time import time


def generate_crack_lines(image, center, num_rings=8, num_cracks_per_ring=100):
    """Generates multiple sets of crack lines in concentric circles, each with full text."""
    height, width, _ = image.shape
    overlay = image.copy()
    max_radius = min(width, height) // 2 - 10
    text = "VAPORWAVE IS DEAD"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1
    text_color = (255, 0, 255)

    for ring in range(1, num_rings + 1):
        radius = int((ring / num_rings) * max_radius)

        for _ in range(num_cracks_per_ring):
            angle = random.uniform(0, 2 * np.pi)
            length = random.randint(20, 80)
            thickness = random.randint(1, 3)

            start_x = int(center[0] + radius * np.cos(angle))
            start_y = int(center[1] + radius * np.sin(angle))
            end_x = int(start_x + length * np.cos(angle))
            end_y = int(start_y + length * np.sin(angle))

            cv2.line(overlay, (start_x, start_y), (end_x, end_y), (0, 0, 0), thickness)

            # Place the full phrase along the crack line
            text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
            text_x = start_x - text_size[0] // 2
            text_y = start_y + text_size[1] // 2
            cv2.putText(overlay, text, (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

    return cv2.addWeighted(overlay, 0.6, image, 0.4, 0)


def apply_circular_glitch(image, center, num_rings=8):
    """Applies glitch effects separately to each concentric circle."""
    glitched_image = image.copy()
    height, width, _ = image.shape
    max_radius = min(width, height) // 2 - 10
    mask = np.zeros((height, width), dtype=np.uint8)

    for ring in range(1, num_rings + 1):
        radius = int((ring / num_rings) * max_radius)
        cv2.circle(mask, center, radius, 255, thickness=30)

        shift = random.randint(-1000, 1000)
        glitched_region = np.roll(glitched_image, shift, axis=random.choice([0, 1]))

        glitched_image[mask == 255] = glitched_region[mask == 255]
        mask.fill(0)  # Reset mask for the next ring

    return glitched_image


def simulate_broken_lcd(image_path):
    """Combines cracks, circular glitches, and text effects to simulate a broken LCD."""
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    center = (width // 2, height // 2)

    image = generate_crack_lines(image, center)
    image = apply_circular_glitch(image, center)

    return image


# Use this image path in all scripts
image_path = "C:/Users/misko/PycharmProjects/glitch-art-app/source-imgs/birds2.jpg"

broken_image = simulate_broken_lcd(image_path)


# Convert cv2 image (BGR) to RGB
broken_image_rgb = cv2.cvtColor(broken_image, cv2.COLOR_BGR2RGB)

# Convert to Pillow Image
pil_image = Image.fromarray(broken_image_rgb)

pil_image.save(f"pallette-out/chatgpt/{time()}.jpg")
print(f"Saved image")


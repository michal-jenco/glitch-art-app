import numpy as np
from PIL import Image, ImageFilter
import cv2


def apply_crt_effect(image_path, scanline_intensity=0.3, glow_intensity=1.0, distortion_factor=0.05,
                     outline_thickness=3, moshing_intensity=0.2, dithering=True):
    # Load the image
    image = Image.open(image_path)

    # Apply Scanlines Effect
    scanline_image = apply_scanlines(image, scanline_intensity)

    # Apply Glow Effect
    glow_image = apply_glow(scanline_image, glow_intensity)

    # Apply Distortion Effect
    distorted_image = apply_distortion(glow_image, distortion_factor)

    # Add Red Outline Effect
    outlined_image = add_red_outline(distorted_image, outline_thickness)

    # Apply Datamoshing Effect
    datamoshed_image = apply_datamoshing(outlined_image, moshing_intensity)

    # Apply Dithering Effect (if enabled)
    if dithering:
        datamoshed_image = apply_dithering(datamoshed_image)

    return datamoshed_image


def apply_scanlines(image, intensity=0.3):
    # Convert to numpy array
    img_array = np.array(image)

    # Apply scanlines (darken every few rows)
    for y in range(0, img_array.shape[0], 4):
        img_array[y] = img_array[y] * (1 - intensity)  # Darken scanline rows

    # Convert back to Image
    return Image.fromarray(img_array)


def apply_glow(image, intensity=1.0):
    # Apply a subtle blur to simulate glow
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=intensity))

    return blurred_image


def apply_distortion(image, distortion_factor=0.05):
    # Convert to numpy array
    img_array = np.array(image)

    # Distortion: Slight warping of the image to simulate CRT curvature
    rows, cols, _ = img_array.shape
    distortion_map = np.random.normal(scale=distortion_factor, size=(rows, cols))

    # Apply the distortion to the image array (simple x-axis bending effect)
    for i in range(rows):
        for j in range(cols):
            offset = int(distortion_map[i, j] * 10)
            new_j = min(max(j + offset, 0), cols - 1)
            img_array[i, j] = img_array[i, new_j]

    return Image.fromarray(img_array)


def add_red_outline(image, outline_thickness=3):
    # Convert image to numpy array
    img_array = np.array(image)

    # Convert to grayscale for edge detection
    gray_image = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

    # Apply edge detection (Canny edge detector)
    edges = cv2.Canny(gray_image, 100, 200)

    # Create a red mask where edges are found
    red_outline = np.zeros_like(img_array)
    red_outline[edges != 0] = [255, 0, 0]  # Red color for edges

    # Blend the red outline with the original image
    blended_image = cv2.addWeighted(img_array, 1.0, red_outline, 0.7, 0)

    # Convert back to Image
    return Image.fromarray(blended_image)


def apply_datamoshing(image, intensity=0.2):
    # Convert to numpy array
    img_array = np.array(image)
    rows, cols, _ = img_array.shape

    # Number of rows to 'mosh' or distort
    num_moshes = int(rows * intensity)

    # Apply a datamoshing effect by shifting chunks of pixels vertically
    for i in range(num_moshes):
        # Randomly choose a vertical slice of the image
        start_row = np.random.randint(0, rows - 10)
        end_row = start_row + np.random.randint(5, 30)

        # Apply a pixel shift to this slice (to create the "mosh" effect)
        shift_amount = np.random.randint(-50, 50)  # Random horizontal shift

        # Shift the selected portion of the image
        img_array[start_row:end_row] = np.roll(img_array[start_row:end_row], shift_amount, axis=1)

    # Convert back to Image
    return Image.fromarray(img_array)


def apply_dithering(image):
    # Convert the image to grayscale first
    grayscale_image = image.convert('L')
    img_array = np.array(grayscale_image)

    # Floyd-Steinberg Dithering Algorithm
    rows, cols = img_array.shape
    for y in range(rows):
        for x in range(cols):
            old_pixel = img_array[y, x]
            new_pixel = 255 * (old_pixel // 128)  # Quantize to either 0 or 255
            img_array[y, x] = new_pixel
            quant_error = old_pixel - new_pixel

            # Distribute error to neighboring pixels (Floyd-Steinberg)
            if x + 1 < cols:
                img_array[y, x + 1] += quant_error * 7 / 16
            if y + 1 < rows:
                img_array[y + 1, x] += quant_error * 5 / 16
                if x + 1 < cols:
                    img_array[y + 1, x + 1] += quant_error * 3 / 16
                if x - 1 >= 0:
                    img_array[y + 1, x - 1] += quant_error * 1 / 16

    # Convert back to image
    return Image.fromarray(img_array)


# Example usage
image_path = "C:/Users/misko/PycharmProjects/glitch-art-app/source-imgs/birds1.jpg"
output_image = apply_crt_effect(image_path, scanline_intensity=0, glow_intensity=0, distortion_factor=0,
                                outline_thickness=3, moshing_intensity=0, dithering=True)

# Show the result
output_image.show()









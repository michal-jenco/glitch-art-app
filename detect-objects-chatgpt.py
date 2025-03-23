import random
import math
from PIL import Image, ImageDraw, ImageFilter


# Function to simulate shattered broken LCD effect with more random cracks
def shattered_broken_lcd_effect(image_path, output_path):
    # Open the image
    img = Image.open(image_path)
    w, h = img.size

    # Create a drawing context
    draw = ImageDraw.Draw(img)

    # Add random jagged cracks and noise
    for _ in range(random.randint(10, 2000)):  # Random number of cracks
        # Random start and end points for the crack line
        start_x = random.randint(0, w)
        start_y = random.randint(0, h)
        end_x = random.randint(0, w)
        end_y = random.randint(0, h)

        # Create jagged crack path by adding random offsets
        crack_path = [(start_x, start_y)]
        for _ in range(random.randint(5, 10)):  # Random segments in the crack
            x_offset = random.randint(-20, 20)
            y_offset = random.randint(-20, 20)
            last_x, last_y = crack_path[-1]
            crack_path.append((last_x + x_offset, last_y + y_offset))

        # Draw the jagged crack
        draw.line(crack_path, fill=(255, 255, 255), width=random.randint(2, 14))

        # Add some random noise particles along the crack
        for _ in range(random.randint(50, 100)):  # Random particles within the crack area
            # Random positions along the crack path
            crack_point = random.choice(crack_path)
            noise_x, noise_y = crack_point
            img.putpixel((noise_x % w, noise_y % h), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # Simulate shattered fragments inside the cracks
    for _ in range(random.randint(3, 6)):  # Random number of broken shards
        # Random position and size of the shattered pieces
        x = random.randint(50, w - 50)
        y = random.randint(50, h - 50)
        size = random.randint(30, 100)

        # Create random shattered pieces (rectangular fragments)
        for _ in range(random.randint(15, 30)):  # Random number of fragments
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, size)
            px = int(x + distance * math.cos(angle))
            py = int(y + distance * math.sin(angle))
            img.putpixel((px, py), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # Apply a distortion filter to simulate the screen's broken state
    img = img.filter(ImageFilter.GaussianBlur(radius=1))  # Optional: blur to simulate distortion

    # Save the result
    img.save(output_path)

    # Display the image with shattered effect
    img.show()


# Test the function
image_path = "C:/Users/misko/PycharmProjects/glitch-art-app/source-imgs/birds1.jpg"
shattered_broken_lcd_effect(image_path, 'output_shattered_broken_lcd.jpg')

# Copyright 2025
# Author: Michal Jenčo
# Email: michal.jenco.brno@gmail.com


import pygame
from pygame import gfxdraw
import sys
import math

from helper_functions import generate_palette

pygame.init()

# Window setup
BASE_SIZE = 300
WIDTH, HEIGHT = BASE_SIZE * 2, BASE_SIZE * 3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Line of Rectangles")

# Color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (80, 160, 255)

# Rectangle setup
rect_width = 40
rect_height = 120
spacing = 20  # space between rectangles
start_x = 50
y_pos = HEIGHT // 2 - rect_height // 2

palette = generate_palette(4, group=True)


def draw_rectangle(x, y, width, height, color, rotation=0):
    """Draw a rectangle, centered at x, y.

    Arguments:
      x (int/float):
        The x coordinate of the center of the shape.
      y (int/float):
        The y coordinate of the center of the shape.
      width (int/float):
        The width of the rectangle.
      height (int/float):
        The height of the rectangle.
      color (str):
        Name of the fill color, in HTML format.
    """
    points = []

    # The distance from the center of the rectangle to
    # one of the corners is the same for each corner.
    radius = math.sqrt((height / 2)**2 + (width / 2)**2)

    # Get the angle to one of the corners with respect
    # to the x-axis.
    angle = math.atan2(height / 2, width / 2)

    # Transform that angle to reach each corner of the rectangle.
    angles = [angle, -angle + math.pi, angle + math.pi, -angle]

    # Convert rotation from degrees to radians.
    rot_radians = (math.pi / 180) * rotation

    # Calculate the coordinates of each point.
    for angle in angles:
        y_offset = -1 * radius * math.sin(angle + rot_radians)
        x_offset = radius * math.cos(angle + rot_radians)
        points.append((x + x_offset, y + y_offset))

    pygame.draw.polygon(screen, color, points)
    gfxdraw.aapolygon(screen, color, points)


# Main loop
running = True
while running:
    screen.fill(BLACK)

    # Draw line of rectangles
    for i in range(30):
        draw_rectangle(400, i * 20 + 50, 3, 50, palette[i % 4], i * 12)

    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()

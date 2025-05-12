import random

import pygame
import math
import sys
from time import time

from palettes import basic_colors

# Define 3D point rotation
def rotate_point(x, y, z, ax, ay, az):
    # Convert degrees to radians
    ax = math.radians(ax)
    ay = math.radians(ay)
    az = math.radians(az)

    # Rotate around X
    cos_x, sin_x = math.cos(ax), math.sin(ax)
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x

    # Rotate around Y
    cos_y, sin_y = math.cos(ay), math.sin(ay)
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y

    # Rotate around Z
    cos_z, sin_z = math.cos(az), math.sin(az)
    x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z

    return x, y, z

# Project 3D point to 2D
def project(x, y, z, width, height, scale=200):
    factor = scale / (z + 5)
    x = int(width / 2 + x * factor)
    y = int(height / 2 - y * factor)
    return x, y

# Draw cube wireframe
def draw_cube(screen, rotation=(0, 0, 0), color=(255, 0, 255)):
    vertices = [
        [-1, -1, -1], [1, -1, -1],
        [1, 1, -1], [-1, 1, -1],
        [-1, -1, 1], [1, -1, 1],
        [1, 1, 1], [-1, 1, 1]
    ]

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # back face
        (4, 5), (5, 6), (6, 7), (7, 4),  # front face
        (0, 4), (1, 5), (2, 6), (3, 7)   # connecting edges
    ]

    points = []
    for x, y, z in vertices:
        rx, ry, rz = rotate_point(x, y, z, *rotation)
        px, py = project(rx, ry, rz, screen.get_width(), screen.get_height())
        points.append((px, py))

    color = random.choice(basic_colors)
    for edge in edges:
        pygame.draw.line(screen, color, points[edge[0]], points[edge[1]], 5)

# Main loop
def run_cube(rotation=(30, 30, 0), color=(0, 255, 255)):
    pygame.init()
    screen = pygame.display.set_mode((200, 200))
    pygame.display.set_caption("Pixelated Wireframe Cube")
    clock = pygame.time.Clock()

    angle = list(rotation)

    frame = 0
    screen_fill = (10, 10, 10)

    while True:
        screen.fill(screen_fill)
        draw_cube(screen, tuple(angle), color)

        frame_path = f"pallette-out/3d-cube/{int(time())}-{frame}.jpg"
        pygame.image.save(screen, frame_path)

        pygame.display.flip()
        clock.tick(15)

        for i, _ in enumerate(angle):
            angle[i] += random.randint(0, 10)

        # Exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        frame += 1

# Example usage
if __name__ == "__main__":
    run_cube(rotation=(45, 30, 10), color=(255, 100, 200))


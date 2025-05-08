import pygame
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Color Palette Visualizer")

# Set up basic font
font = pygame.font.SysFont(None, 24)

# Color mapping similar to what was used in old BASIC palette (simplified)
basic_colors = [
    (0, 0, 0),       # 0: black
    (0, 0, 128),     # 1: dark blue
    (0, 128, 0),     # 2: dark green
    (0, 128, 128),   # 3: dark cyan
    (128, 0, 0),     # 4: dark red
    (128, 0, 128),   # 5: dark magenta
    (128, 128, 0),   # 6: dark yellow
    (192, 192, 192), # 7: light gray
    (128, 128, 128), # 8: dark gray
    (0, 0, 255),     # 9: blue
    (0, 255, 0),     # 10: green
    (0, 255, 255),   # 11: cyan
    (255, 0, 0),     # 12: red
    (255, 0, 255),   # 13: magenta
    (255, 255, 0),   # 14: yellow
    (255, 255, 255), # 15: white
]

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))

    for i in range(16):
        x = (i % 8) * 80 + 40
        y = (i // 8) * 200 + 100

        # Draw color box
        pygame.draw.rect(screen, basic_colors[i], (x, y, 60, 60))

        # Draw color index label
        label = font.render(str(i), True, (255, 255, 255))
        screen.blit(label, (x + 20, y + 70))

    pygame.display.flip()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()

import sys
import time

import numpy as np
import pygame


def render_object_display_text(object_mass, fx_total, fy_total,
                               object_vx, object_vy, object_px, object_py):
    mass_text = f'M={object_mass}'
    force_text = f'F=({fx_total.__round__(2)},{fy_total.__round__(2)})'
    velocity_text = f'V=({object_vx.__round__(2)},{object_vy.__round__(2)})'
    text_str = f'{mass_text}  {force_text}  {velocity_text}'

    text = font.render(text_str, True, BLUE)
    textRect.center = (object_px + object_mass + 10, object_py + object_mass + 10)

    screen.blit(text, textRect)


G = 6.67408e-11 * 100_000_000  # Otherwise the bodies would not move given the small value of gravitational constant
NUM_OF_BODIES = 10
WIDTH = 800
HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (109, 196, 255)

vx = np.zeros((NUM_OF_BODIES,), dtype=float)
vy = np.zeros((NUM_OF_BODIES,), dtype=float)

px = np.random.uniform(low=10, high=WIDTH - 10, size=NUM_OF_BODIES)
py = np.random.uniform(low=10, high=HEIGHT - 10, size=NUM_OF_BODIES)

m = np.random.randint(1, 25, size=NUM_OF_BODIES)

fx = np.zeros((NUM_OF_BODIES,), dtype=float)
fy = np.zeros((NUM_OF_BODIES,), dtype=float)

pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

font = pygame.font.SysFont('Arial', 12)
text = font.render('0', True, BLUE)
textRect = text.get_rect()
while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    in_t = time.time()
    for i in range(0, NUM_OF_BODIES):
        xdiff = (px - px[i])
        ydiff = (py - py[i])

        distance = np.sqrt(xdiff ** 2 + ydiff ** 2)

        f = G * m[i] * np.divide(m, distance ** 2)

        sin = np.divide(ydiff, distance)
        cos = np.divide(xdiff, distance)

        fx_total = np.nansum(np.multiply(f, cos))
        fy_total = np.nansum(np.multiply(f, sin))

        vx[i] = vx[i] + fx_total / m[i]
        vy[i] = vy[i] + fy_total / m[i]

        px[i] = px[i] + vx[i]
        py[i] = py[i] + vy[i]

        # Comment this method call to remove the text information over objects
        render_object_display_text(m[i], fx_total, fy_total, vx[i], vy[i], px[i], py[i])

        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(px[i], py[i], m[i], m[i]))
    print(time.time() - in_t)
    pygame.display.flip()

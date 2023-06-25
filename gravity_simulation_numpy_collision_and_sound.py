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
NUM_OF_BODIES = 5
WIDTH = 800
HEIGHT = 640
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (109, 196, 255)

vx = np.zeros((NUM_OF_BODIES,), dtype=float)
vy = np.zeros((NUM_OF_BODIES,), dtype=float)

px = np.random.uniform(low=10, high=WIDTH - 10, size=NUM_OF_BODIES)
py = np.random.uniform(low=10, high=HEIGHT - 10, size=NUM_OF_BODIES)

m = np.random.randint(13, 15, size=NUM_OF_BODIES)

rects = [pygame.Rect(px[i], py[i], m[i], m[i]) for i in range(NUM_OF_BODIES)]

fx = np.zeros((NUM_OF_BODIES,), dtype=float)
fy = np.zeros((NUM_OF_BODIES,), dtype=float)

t_vx = vx.copy()
t_vy = vy.copy()
t_px = px.copy()
t_py = py.copy()

pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

font = pygame.font.SysFont('Arial', 12)
text = font.render('0', True, BLUE)
textRect = text.get_rect()
crash_sound = pygame.mixer.Sound("audio/collision_00_comp.mp3")
rgb = (255, 255, 255)
while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    in_t = time.time()
    for i in range(0, NUM_OF_BODIES):
        xdiff = (px - px[i])
        ydiff = (py - py[i])

        indices = rects[i].collidelistall(rects)
        indices.remove(i)
        c_vx = 0
        c_vy = 0

        for two in indices:
            pygame.mixer.Channel(0).play(crash_sound)
            mass_sum = m[i] + m[two]
            mass_diff = m[i] - m[two]
            twice_mass_two = 2 * m[two]
            c_vx += ((mass_diff / mass_sum) * vx[i]) + ((twice_mass_two / mass_sum) * vx[two])
            c_vy += ((mass_diff / mass_sum) * vy[i]) + ((twice_mass_two / mass_sum) * vy[two])

        distance = np.sqrt(xdiff ** 2 + ydiff ** 2)

        f = G * m[i] * np.divide(m, distance)

        sin = np.divide(ydiff, distance)
        cos = np.divide(xdiff, distance)

        fx_total = np.nansum(np.multiply(f, cos))
        fy_total = np.nansum(np.multiply(f, sin))

        # If collision does not occur, calculate the for
        if not c_vx:
            c_vx = c_vx + vx[i] + fx_total / m[i]
        if not c_vy:
            c_vy = c_vy + vy[i] + fy_total / m[i]

        if t_px[i] - m[i] < 0 or t_px[i] + m[i] > WIDTH:
            c_vx = -c_vx
            pygame.mixer.Channel(1).play(crash_sound)

        if t_py[i] - m[i] < 0 or t_py[i] + m[i] > HEIGHT:
            c_vy = -c_vy
            pygame.mixer.Channel(1).play(crash_sound)

        # Limit the velocities to avoid erratic behavior
        # if c_vx > 3.0:
        #     c_vx = 3.0
        # if c_vx < -3.0:
        #     c_vx = -3.0
        # if c_vy > 3.0:
        #     c_vy = 3.0
        # if c_vy < -3.0:
        #     c_vy = -3.0

        t_px[i] = px[i] + c_vx
        t_py[i] = py[i] + c_vy

        t_vx[i] = c_vx
        t_vy[i] = c_vy

        # Comment this method call to remove the text information over objects
        # render_object_display_text(m[i], fx_total, fy_total, vx[i], vy[i], px[i], py[i])

        # pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(px[i], py[i], m[i], m[i]))
    # Update px, py, vx, vy
    px = t_px.copy()
    py = t_py.copy()
    vx = t_vx.copy()
    vy = t_vy.copy()

    for i in range(NUM_OF_BODIES):
        rects[i].left = px[i]
        rects[i].top = py[i]
        pygame.draw.rect(screen, rgb, rects[i])

    # print(time.time() - in_t)
    pygame.display.flip()

# Very simple implementation of simulation of gravity on bodies in 2D. Does not handle the case when 2 or more
# bodies collide with each other
import random
import math
import sys
import pygame
import numpy as np


G = (
    6.67408e-11 * 100_000_000
)  # Otherwise the bodies would not move given the small value of gravitational constant
NUM_OF_BODIES = 10
WIDTH = 900
HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (109, 196, 255)

x = np.random.randint(10, WIDTH - 10, NUM_OF_BODIES).astype(np.float32)
y = np.random.randint(10, HEIGHT - 10, NUM_OF_BODIES).astype(np.float32)
v_x = np.zeros(NUM_OF_BODIES, dtype=np.float32)
v_y = np.zeros(NUM_OF_BODIES, dtype=np.float32)
m = np.random.randint(1, 25, NUM_OF_BODIES).astype(np.float32)

# Some predefined bodies for the purpose of testing
# bodies.append(Body([500,500],[0,0],[0,0],20))
# bodies.append(Body([510,503],[0,0],[0,0],7))
# bodies.append(Body([400,400],[0,0],[0,0],14))
# bodies.append(Body([10,600],[0,0],[0,0],9))
# bodies.append(Body([250,198],[0,0],[0,0],18))
# bodies.append(Body([340,700],[0,0],[0,0],24))

pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

font = pygame.font.SysFont("Arial", 16)
text = font.render("0", True, BLUE)
textRect = text.get_rect()
while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    fx_total = np.zeros(NUM_OF_BODIES)
    fy_total = np.zeros(NUM_OF_BODIES)

    x_diff = np.repeat(x[:, np.newaxis], NUM_OF_BODIES, axis=1) - np.repeat(
        x[np.newaxis, :], NUM_OF_BODIES, axis=0
    )
    y_diff = np.repeat(y[:, np.newaxis], NUM_OF_BODIES, axis=1) - np.repeat(
        y[np.newaxis, :], NUM_OF_BODIES, axis=0
    )
    hypotenuse = np.sqrt(x_diff ** 2 + y_diff ** 2)
    hypotenuse[np.diag_indices(NUM_OF_BODIES)] = np.inf

    sin = x_diff / hypotenuse
    cos = y_diff / hypotenuse
    f = -G * m[np.newaxis, :] * m[:, np.newaxis] / hypotenuse ** 2
    fx = f * sin
    fy = f * cos

    v_x += np.sum(fx, axis=1) / m
    v_y += np.sum(fy, axis=1) / m

    x += v_x
    y += v_y

    for idx in range(NUM_OF_BODIES):
        mass_text = "M={0}".format(m[idx])
        # force_text = 'F=({0},{1})'.format(fx_total.__round__(3), fy_total.__round__(3))
        # velocity_text = 'V=({},{})'.format(body_a.v[0].__round__(3),body_a.v[1].__round__(3))
        # text_str = mass_text + '   ' + force_text + '   ' + velocity_text
        text_str = mass_text

        text = font.render(text_str, True, BLUE)
        textRect.center = (x[idx] + m[idx] + 10, y[idx] + m[idx] + 10)

        screen.blit(text, textRect)
        pygame.draw.rect(
            screen, (255, 255, 255), pygame.Rect(x[idx], y[idx], m[idx], m[idx])
        )
    pygame.display.flip()

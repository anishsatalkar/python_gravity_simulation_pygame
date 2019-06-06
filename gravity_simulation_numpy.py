import sys
import time

import numpy as np
import pygame

G = 6.67408e-11 * 100_000_000  # Otherwise the bodies would not move given the small value of gravitational constant
NUM_OF_BODIES = 4000
WIDTH = 1200
HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (109, 196, 255)

vx = np.zeros((NUM_OF_BODIES,),dtype=np.float)
vy = np.zeros((NUM_OF_BODIES,),dtype=np.float)

px = np.random.uniform(low=10, high=WIDTH-10,size=NUM_OF_BODIES)
py = np.random.uniform(low=10, high=HEIGHT-10,size=NUM_OF_BODIES)

m = np.random.randint(1,25,size=NUM_OF_BODIES)

fx = np.zeros((NUM_OF_BODIES,),dtype=float)
fy = np.zeros((NUM_OF_BODIES,),dtype=float)


pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

font = pygame.font.SysFont('Arial', 16)
text = font.render('0', True, BLUE)
textRect = text.get_rect()
while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    in_t = time.time()
    for i in range(0,NUM_OF_BODIES):
        xdiff = (px - px[i])
        ydiff = (py - py[i])


        distance = np.sqrt(xdiff ** 2 + ydiff ** 2)

        f = G * m[i] * np.divide(m,distance ** 2)


        sin = np.divide(ydiff,distance)
        cos = np.divide(xdiff,distance)

        fx_total = np.nansum(np.multiply(f, cos))
        fy_total = np.nansum(np.multiply(f,sin))

        vx[i] = vx[i] + fx_total / m[i]
        vy[i] = vy[i] + fy_total / m[i]

        px[i] = px[i] + vx[i]
        py[i] = py[i] + vy[i]


        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(px[i], py[i], m[i],m[i]))
    print(time.time() - in_t)
    pygame.display.flip()

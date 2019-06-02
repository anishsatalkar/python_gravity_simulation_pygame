# Very simple implementation of simulation of gravity on bodies in 2D. Does not handle the case when 2 or more
# bodies collide with each other

import math
import sys, pygame
from scipy.constants import gravitational_constant

G = gravitational_constant * 100000000

class Body:
    def __init__(self, pos, a, v, m):
        self.pos = pos  # pos is a list of x and y position of that body in pixels eg : [500,600]
        self.a = a  # a is a list of x and y components of accelaration of that body in pixel units
        self.v = v  # b is a list of x and y components of velocity of that body in pixel units
        self.m = m  # m is the mass of that object
        self.size = [m, m]  # size is used for only visualisation of the body


def calculate_forces(pos_a, pos_b, m_a, m_b):
    x_diff = pos_b[0] - pos_a[0]
    y_diff = pos_b[1] - pos_a[1]
    f = G * m_a * m_b / math.sqrt((x_diff) ** 2 + (y_diff) ** 2)
    angle = math.atan2(y_diff, x_diff)
    fx = f * math.cos(angle)
    fy = f * math.sin(angle)

    return fx, fy


b1 = Body([500, 500], [0, 0], [0, 0], 20)
b2 = Body([100, 200], [0, 0], [0, 0], 2.4)
b3 = Body([250, 478], [0, 0], [0, 0], 7)
b4 = Body([50, 500], [0, 0], [0, 0], 1)

bodies = [b1, b2, b3, b4]

pygame.init()

size = width, height = 800, 700
black = 0, 0, 0

screen = pygame.display.set_mode(size)

white = (255, 255, 255)

font = pygame.font.SysFont('Arial', 16)

text = font.render('0', True, white)
textRect = text.get_rect()

while 1:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    for body_a in bodies:
        pos_a = body_a.pos
        m_a = body_a.m
        fx_total = 0
        fy_total = 0

        for body_b in bodies:
            if body_b.pos == pos_a:
                continue
            fx, fy = calculate_forces(pos_a, body_b.pos, m_a, body_b.m)
            fx_total += fx
            fy_total += fy

        body_a_acceleration = body_a.a

        body_a_acceleration[0] = fx_total / m_a
        body_a_acceleration[1] = fy_total / m_a

        body_a.v[0] = body_a.v[0] + body_a_acceleration[0]
        body_a.v[1] = body_a.v[1] + body_a_acceleration[1]

        pos_a[0] = pos_a[0] + body_a.v[0]
        pos_a[1] = pos_a[1] + body_a.v[1]

        text_str = 'm=' + str(m_a)

        # Use this text_str to display the x and y components of forces acting on that body
        # text_str = 'm=' + str(m_a) + ' , f=' + str(fx_total.__round__(3)) + ' , ' + str(fy_total.__round__(3))

        body_a_size = body_a.size

        text = font.render(text_str, True, white)
        textRect.center = (
            pos_a[0] + body_a_size[0] + 10, pos_a[1] + body_a_size[1] + 10)

        screen.blit(text, textRect)

        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(pos_a[0], pos_a[1], body_a.size[0], body_a.size[1]))

    pygame.display.flip()

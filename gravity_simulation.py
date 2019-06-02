# Very simple implementation of simulation of gravity on bodies in 2D. Does not handle the case when 2 or more
# bodies collide with each other
import random
import math
import sys
import pygame


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


gravitational_constant = 6.67408e-11
G = gravitational_constant * 100000000  # Otherwise the bodies would not move given the small value of gravitational
# constant
NUM_OF_BODIES = 10
WIDTH = 1280
HEIGHT = 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (109, 196, 255)

bodies = []
for i in range(NUM_OF_BODIES):
    px = random.randint(10, WIDTH - 10)
    py = random.randint(10, HEIGHT - 10)
    m = random.randint(1, 25)
    bodies.append(Body([px, py], [0, 0], [0, 0], m))

pygame.init()

size = WIDTH, HEIGHT

screen = pygame.display.set_mode(size)

font = pygame.font.SysFont('Arial', 16)

text = font.render('0', True, BLUE)
textRect = text.get_rect()

while 1:
    screen.fill(BLACK)
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

        mass_text = 'm={0}'.format(m_a)
        force_text = 'f=({0},{1})'.format(fx_total.__round__(3), fy_total.__round__(3))
        text_str = mass_text + ' | ' + force_text

        body_a_size = body_a.size

        text = font.render(text_str, True, BLUE)
        textRect.center = (
            pos_a[0] + body_a_size[0] + 10, pos_a[1] + body_a_size[1] + 10)

        screen.blit(text, textRect)

        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(pos_a[0], pos_a[1], body_a.size[0], body_a.size[1]))

    pygame.display.flip()

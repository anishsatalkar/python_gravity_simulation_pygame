# Very simple implementation of simulation of gravity on bodies in 2D. Does not handle the case when 2 or more
# bodies collide with each other
import random
import sys
import math
import pygame

from Planet import Body

if __name__ == "__main__":
    NUM_OF_BODIES = 20
    WIDTH = 900
    HEIGHT = 800
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (109, 196, 255)

    bodies = []
    for i in range(NUM_OF_BODIES):
        px = random.randint(10, WIDTH - 10)
        py = random.randint(10, HEIGHT - 10)
        m = random.randint(1, 20)
        bodies.append(Body([px, py], [0, 0], m, i))

    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    font = pygame.font.SysFont('Arial', 16)
    text = font.render('0', True, BLUE)
    textRect = text.get_rect()
    velocity_diff = [0, 0]
    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Don't process bodies that where hit/removed
        bodies = [body for body in bodies if not body.hit]

        # Get Bodies and find the center of mass of all
        x = [p.pos[0] for p in bodies]
        y = [p.pos[1] for p in bodies]
        centroid = (sum(x) / len(bodies), sum(y) / len(bodies))
        lx = bodies[0].pos[0]
        ly = bodies[0].pos[1]
        for body in bodies:
            body.pos[0] = body.pos[0] - centroid[0] + WIDTH / 2
            body.pos[1] = body.pos[1] - centroid[1] + HEIGHT / 2

        # Draw circles and line for reference point of origin
        velocity_diff[0] = lx - centroid[0]
        velocity_diff[1] = ly - centroid[1]
        # Origin Point
        textRect.center = (velocity_diff[0] + 10, velocity_diff[1] + 10)
        screen.blit(font.render("{0},{1}".format(0, 0), True, BLUE), textRect)
        pygame.draw.circle(screen, (255, 255, 127), [int(velocity_diff[0]), int(velocity_diff[1])], 3, 1)
        # Center of all objects
        textRect.center = (WIDTH/2 + 10, HEIGHT/2 + 10)
        screen.blit(font.render("{0},{1}".format(
            int(math.floor(velocity_diff[0])),
            int(math.floor(velocity_diff[1]))), True, BLUE), textRect)
        # Draw line from origin to center of all objects
        pygame.draw.line(screen, (255, 255, 0), (WIDTH/2, HEIGHT/2), velocity_diff)
        pygame.draw.circle(screen, (255, 255, 127), [int(WIDTH/2), int(HEIGHT/2)], 3, 1)

        for body_a in bodies:
            # Remove invulnerability flag
            body_a.invuln = False

            f_totals = body_a.n_body(bodies, 0, 0)

            body_a.velocity[0] = body_a.velocity[0] + f_totals[0] / body_a.mass
            body_a.velocity[1] = body_a.velocity[1] + f_totals[1] / body_a.mass

            body_a.pos[0] = body_a.pos[0] + body_a.velocity[0]
            body_a.pos[1] = body_a.pos[1] + body_a.velocity[1]

            mass_text = 'M={0}'.format(body_a.mass)
            # force_text = 'F=({0},{1})'.format(fx_total.__round__(3), fy_total.__round__(3))
            # velocity_text = 'V=({},{})'.format(body_a.v[0].__round__(3),body_a.v[1].__round__(3))
            # text_str = mass_text + '   ' + force_text + '   ' + velocity_text
            text_str = mass_text

            text = font.render(text_str, True, BLUE)
            textRect.center = (
                body_a.pos[0] + body_a.size + 10,
                body_a.pos[1] + body_a.size + 10)

            screen.blit(text, textRect)

            pygame.draw.circle(
                screen,
                (255, 255, 255),
                [int(body_a.pos[0]), int(body_a.pos[1])], int(body_a.size))

            # Get a list of bodies, except for body_a
            next_bodies = [body for body in bodies if not body_a.id == body.id]
            for body in next_bodies:
                # if body is invulnerable then continue on to the next body
                if body.invuln:
                    continue
                # Find the distance to body_a
                distance = math.sqrt(
                    ((body_a.pos[0] - body.pos[0]) * (body_a.pos[0] - body.pos[0])) +
                    ((body_a.pos[1] - body.pos[1]) * (body_a.pos[1] - body.pos[1])))
                # If bodied touch then "remove" one by setting flag and making the other invulnerable
                if distance < int(body_a.size) + int(body.size):
                    if body_a.mass >= body.mass:
                        body_a.mass += body.mass
                        body_a.update_size()
                        body_a.velocity[0] = (body_a.mass * body_a.velocity[0] + body.mass * body.velocity[0]
                                              ) / (body_a.mass + body.mass)
                        body_a.velocity[1] = (body_a.mass * body_a.velocity[1] + body.mass * body.velocity[1]
                                              ) / (body_a.mass + body.mass)
                        body.hit = True
                        body_a.invuln = True
                    else:
                        body.mass += body_a.mass
                        body.update_size()
                        body.velocity[0] = (body_a.mass * body_a.velocity[0] + body.mass * body.velocity[0]
                                            ) / (body_a.mass + body.mass)
                        body.velocity[1] = (body_a.mass * body_a.velocity[1] + body.mass * body.velocity[1]
                                            ) / (body_a.mass + body.mass)
                        body_a.hit = True
                        body.invuln = True
        pygame.display.flip()

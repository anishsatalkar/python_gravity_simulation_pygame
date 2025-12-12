import sys
import time

import numpy as np
import pygame

from world import World


class NBodySimulator:
    # Gravitational constant. Multiplied by 100M so that the bodies can move given the small value of
    # gravitational constant
    G = 6.67408e-11 * 100_000_000

    # Width of the window.
    WIDTH = 800

    # Height of the window.
    HEIGHT = 640

    # RGB for white.
    WHITE = (255, 255, 255)

    # RGB for black.
    BLACK = (0, 0, 0)

    # RGB for a color that looks like blue.
    BLUE = (109, 196, 255)

    # Velocity limit
    V_LIMIT = 3

    def __init__(self, world=None):
        pygame.init()
        if not world:
            self.world = World(NBodySimulator.HEIGHT, NBodySimulator.WIDTH)
        else:
            self.world = world
        self.font = pygame.font.SysFont('Arial', 12)
        self.screen = None

    def _render_object_display_text(self, object_mass, fx_total, fy_total,
                                    object_vx, object_vy, object_px, object_py):
        mass_text = f'M={object_mass}'
        force_text = f'F=({fx_total.__round__(2)},{fy_total.__round__(2)})'
        velocity_text = f'V=({object_vx.__round__(2)},{object_vy.__round__(2)})'
        text_str = f'{mass_text}  {force_text}  {velocity_text}'

        text = self.font.render(text_str, True, NBodySimulator.BLUE)
        text_rect = text.get_rect()
        text_rect.center = (object_px + object_mass + 10, object_py + object_mass + 10)
        self.screen.blit(text, text_rect)

    def run_simulation(self):
        """
        This function runs the simulation loop.

        Since there is a costly loop involved, I've refrained from making function calls inside that loop
        to keep the simulation as highly performant as possible and that is one reason why this function is so
        long and ugly.
        :return:
        """
        t_vx = self.world.vx.copy()
        t_vy = self.world.vy.copy()
        t_px = self.world.px.copy()
        t_py = self.world.py.copy()

        pygame.init()
        size = NBodySimulator.WIDTH, NBodySimulator.HEIGHT
        self.screen = pygame.display.set_mode(size)

        crash_sound = pygame.mixer.Sound("audio/collision_00_comp.mp3")
        rgb = [''] * self.world.num_of_bodies

        while True:
            self.screen.fill(NBodySimulator.BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            in_t = time.time()
            for i in range(0, self.world.num_of_bodies):
                xdiff = (self.world.px - self.world.px[i])
                ydiff = (self.world.py - self.world.py[i])

                indices = self.world.rects[i].collidelistall(self.world.rects)
                indices.remove(i)
                c_vx = 0
                c_vy = 0

                for two in indices:
                    pygame.mixer.Channel(0).play(crash_sound)
                    mass_sum = self.world.m[i] + self.world.m[two]
                    mass_diff = self.world.m[i] - self.world.m[two]
                    twice_mass_two = 2 * self.world.m[two]
                    c_vx += ((mass_diff / mass_sum) * self.world.vx[i]) + \
                            ((twice_mass_two / mass_sum) * self.world.vx[two])
                    c_vy += ((mass_diff / mass_sum) * self.world.vy[i]) + \
                            ((twice_mass_two / mass_sum) * self.world.vy[two])

                distance = np.sqrt(xdiff ** 2 + ydiff ** 2)

                f = NBodySimulator.G * self.world.m[i] * np.divide(self.world.m, distance)

                sin = np.divide(ydiff, distance)
                cos = np.divide(xdiff, distance)

                fx_total = np.nansum(np.multiply(f, cos))
                fy_total = np.nansum(np.multiply(f, sin))

                # If collision does not occur, calculate the for
                if not c_vx:
                    c_vx = c_vx + self.world.vx[i] + fx_total / self.world.m[i]
                if not c_vy:
                    c_vy = c_vy + self.world.vy[i] + fy_total / self.world.m[i]

                if t_px[i] - self.world.m[i] < 0 or t_px[i] + self.world.m[i] > NBodySimulator.WIDTH:
                    c_vx = -c_vx
                    pygame.mixer.Channel(1).play(crash_sound)

                if t_py[i] - self.world.m[i] < 0 or t_py[i] + self.world.m[i] > NBodySimulator.HEIGHT:
                    c_vy = -c_vy
                    pygame.mixer.Channel(1).play(crash_sound)

                # Limit the velocities to avoid erratic behavior
                if c_vx > self.V_LIMIT:
                    c_vx = self.V_LIMIT
                if c_vx < -self.V_LIMIT:
                    c_vx = -self.V_LIMIT
                if c_vy > self.V_LIMIT:
                    c_vy = self.V_LIMIT
                if c_vy < -self.V_LIMIT:
                    c_vy = -self.V_LIMIT

                t_px[i] = self.world.px[i] + c_vx
                t_py[i] = self.world.py[i] + c_vy

                t_vx[i] = c_vx
                t_vy[i] = c_vy

                # Comment this method call to remove the text information over objects
                # render_object_display_text(m[i], fx_total, fy_total, vx[i], vy[i], px[i], py[i])

                # pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(px[i], py[i], m[i], m[i]))
                f_sum = abs(fx_total) + abs(fy_total)
                rgb[i] = (min(128 + (f_sum * 1000), 255), min(128 + (f_sum * 5000), 255), max(255 - (f_sum * 2000), 0))
            # Update px, py, vx, vy
            self.world.px = t_px.copy()
            self.world.py = t_py.copy()
            self.world.vx = t_vx.copy()
            self.world.vy = t_vy.copy()

            for i in range(self.world.num_of_bodies):
                self.world.rects[i].left = self.world.px[i]
                self.world.rects[i].top = self.world.py[i]
                pygame.draw.rect(self.screen, rgb[i], self.world.rects[i])

            # print(time.time() - in_t)
            pygame.display.flip()

if __name__ == '__main__':
    NBodySimulator(World(NBodySimulator.HEIGHT, NBodySimulator.WIDTH, 10)).run_simulation()
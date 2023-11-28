import numpy as np
import pygame


class World:
    def __init__(self, height, width, num_of_bodies=2):
        self.num_of_bodies = num_of_bodies
        self._setup_bodies(num_of_bodies, height, width)
        self.rects = [pygame.Rect(self.px[i], self.py[i], self.m[i], self.m[i]) for i in range(self.num_of_bodies)]
        self.fx = np.zeros((self.num_of_bodies,), dtype=float)
        self.fy = np.zeros((self.num_of_bodies,), dtype=float)

    def _setup_bodies(self, num_of_bodies, height, width):
        if num_of_bodies == 2:
            self.vx = np.array([-0.3, 0.3])
            self.vy = np.array([0.0, 0.0])
            self.px = np.array([300.0, 300.0], dtype=float)
            self.py = np.array([300.0, 200.0], dtype=float)
            self.m = np.array([13, 13], dtype=int)
            return
        self.vx = np.zeros((self.num_of_bodies,), dtype=float)
        self.vy = np.zeros((self.num_of_bodies,), dtype=float)
        self.px = np.random.uniform(low=10, high=width - 10, size=(self.num_of_bodies,))
        self.py = np.random.uniform(low=10, high=height - 10, size=(self.num_of_bodies,))
        self.m = np.random.randint(12, 14, size=self.num_of_bodies)
        return


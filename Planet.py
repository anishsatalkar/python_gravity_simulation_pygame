import math

G = 6.67408e-11 * 100_000_000


class Body:
    def __init__(self, pos, velocity, mass, id_num):
        self.pos = pos  # pos is a list of x and y position of that body in pixels eg : [500,600]
        self.velocity = velocity  # b is a list of x and y components of velocity of that body in pixel units
        self.mass = mass  # m is the mass of that object
        self.size = math.log2(self.mass)  # size is used for only visualisation of the body
        self.id = id_num  # id is the unique identifier for this body
        self.hit = False  # tell us if this object was hit by another
        self.invuln = False  # a temporary flag for showing what is invulnerable

    def update_size(self):
        self.size = math.log2(self.mass)

    def n_body(self, other_bodies, n_fx_total, n_fy_total):
        for body_b in other_bodies:
            if body_b.pos != self.pos:
                fx, fy = self.calculate_forces(self.pos, body_b.pos, self.mass, body_b.mass)
                n_fx_total += fx
                n_fy_total += fy
        return [n_fx_total, n_fy_total]

    @staticmethod
    def calculate_forces(c_pos_a: list, c_pos_b: list, c_m_a: float, c_m_b: float):
        x_diff = c_pos_b[0] - c_pos_a[0]
        y_diff = c_pos_b[1] - c_pos_a[1]
        f = G * c_m_a * c_m_b / math.sqrt(x_diff ** 2 + y_diff ** 2)
        angle = math.atan2(y_diff, x_diff)
        cfx = f * math.cos(angle)
        cfy = f * math.sin(angle)
        return cfx, cfy

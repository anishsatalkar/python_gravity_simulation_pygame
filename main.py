from gravity_simulation_numpy_collision_and_sound import NBodySimulator
from world import World


def main():
    world = World(800, 640, 4)
    n_body_simulator = NBodySimulator()
    n_body_simulator.run_simulation()


if __name__ == '__main__':
    main()

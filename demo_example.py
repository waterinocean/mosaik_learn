"""
a simple scenario
"""

import mosaik

META = {
    "AddSim": {"python": "example_model:ExampleSim"},
    "Monitor": {"python": "collector:Monitor"},
}


def main():
    world = mosaik.World(META)

    add_simu = world.start("AddSim")
    add_model = add_simu.Model(init_val=2)

    monitor_simu = world.start("Monitor")
    monitor_model = monitor_simu.Monitor()

    world.connect(add_model, monitor_model, "val")

    world.run(until=6)


if __name__ == "__main__":
    main()

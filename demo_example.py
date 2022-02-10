"""
a simple scenario
"""

import mosaik

META = {
    "AddSim": {"python": "example_model:ExampleSim"},
    "Monitor": {"python": "collector:Monitor"},
    "Controller": {"python": "controller:Controller"},
}


def main():
    world = mosaik.World(META)

    add_simu = world.start("AddSim")
    add_model = add_simu.Model(init_val=2)

    monitor_simu = world.start("Monitor")
    monitor_model = monitor_simu.Monitor()

    controller_simu = world.start("Controller")
    controller_model = controller_simu.Controller()

    world.connect(add_model, controller_model, ("val_out", "val_in"))
    world.connect(controller_model, add_model, ("delta_out", "delta_in"), weak=True)

    world.connect(add_model, monitor_model, "val_out")
    world.connect(controller_model, monitor_model, "delta_out")

    world.run(until=10)


if __name__ == "__main__":
    main()

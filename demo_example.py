"""
a simple scenario
"""

import mosaik
from mosaik.util import connect_many_to_one

META = {
    "AddSim": {"python": "example_model:ExampleSim"},
    "Monitor": {"python": "collector:Monitor"},
    "Controller": {"python": "controller:Controller"},
}


def main():
    world = mosaik.World(META)

    add_simu = world.start("AddSim")
    add_model_list = [add_simu.Model(init_val=i) for i in range(-2, 3, 2)]

    monitor_simu = world.start("Monitor")
    monitor_model = monitor_simu.Monitor()

    controller_simu = world.start("Controller")
    controller_model_list = controller_simu.Controller.create(len(add_model_list))

    for add_model, controller_model in zip(add_model_list, controller_model_list):
        world.connect(add_model, controller_model, ("val_out", "val_in"))
        world.connect(controller_model, add_model, ("delta_out", "delta_in"), weak=True)

    connect_many_to_one(world, add_model_list, monitor_model, "val_out")
    connect_many_to_one(world, controller_model_list, monitor_model, "delta_out")

    # world.connect(add_model, monitor_model, "val_out")
    # world.connect(controller_model, monitor_model, "delta_out")

    world.run(until=10)


if __name__ == "__main__":
    main()

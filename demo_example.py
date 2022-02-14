"""
a simple scenario
"""

import mosaik
from mosaik.util import connect_many_to_one

META = {
    "AddSim": {"python": "example_model:ExampleSim"},
    "Monitor": {"cmd": "%(python)s collector.py 127.0.0.1:5555"},
    "Controller": {"python": "controller:Controller"},
    "MasterController": {"python": "master_controller:MasterController"},
}


def main():
    world = mosaik.World(META, debug=True)

    add_simu = world.start("AddSim")
    add_model_list = [add_simu.Model(init_val=i) for i in range(-2, 3, 2)]

    monitor_simu = world.start("Monitor")
    monitor_model = monitor_simu.Monitor()

    controller_simu = world.start("Controller")
    controller_model_list = controller_simu.Controller.create(len(add_model_list))

    master_controller_simu = world.start("MasterController")
    master_controller_model = master_controller_simu.MasterController()

    for add_model, controller_model in zip(add_model_list, controller_model_list):
        world.connect(add_model, controller_model, ("val_out", "val_in"))
        world.connect(controller_model, add_model, ("delta", "delta_in"), time_shifted=True, initial_data={"delta": 0})

    for controller_model in controller_model_list:
        world.connect(controller_model, master_controller_model, ("delta", "delta_in"))
        world.connect(
            master_controller_model, controller_model, ("delta_out", "delta"), weak=True
        )

    connect_many_to_one(world, add_model_list, monitor_model, "val_out")
    connect_many_to_one(world, controller_model_list, monitor_model, "delta")
    world.connect(master_controller_model, monitor_model, "delta_out")

    print(world.entity_graph.nodes)
    print(world.entity_graph.edges)

    world.run(until=20)

    print(world.execution_graph.nodes)
    print(world.execution_graph.edges)


if __name__ == "__main__":
    main()

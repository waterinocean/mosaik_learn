"""
an controller for add model, when val of add model beyond [-3, 3] then change the delta to 1 or -1
"""

import mosaik_api

META = {
    "type": "event-based",
    "models": {
        "Controller": {"public": True, "params": [], "attrs": ["val_in", "delta_out"]}
    },
}


class Controller(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.entities = {}
        self.eid_prefix = "Controller_"

    def create(self, num, model, **model_params):
        return super().create(num, model, **model_params)

    def step(self, time, inputs, max_advance):
        return super().step(time, inputs, max_advance)

    def get_data(self, outputs):
        return super().get_data(outputs)

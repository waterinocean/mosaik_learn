'''
a simple add operate model, add an delta with an init val and get an output val
'''

import mosaik_api

META = {
    "type": "time-based",
    "models": {
        "Model": {
            "public": True,
            "params": ["init_val"],
            "attrs": ["val", "delta"]
        }
    }
}

class ExampleModel(object):
    def __init__(self, init_val: int = 0) -> None:
        self.init_val = init_val
        self.val = self.init_val

    def step(self, delta: int):
        self.val += delta


class ExampleSim(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = "Model_"
        self.entities = []
        self.data = {}
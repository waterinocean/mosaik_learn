"""
a simple data collector, receive any inputs and print them in the end
"""

import collections
from mosaik_debug import mosaik_api

META = {
    "type": "event-based",
    "models": {
        "Monitor": {"public": True, "any_inputs": True, "params": [], "attrs": []}
    },
}


class Monitor(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid = None
        self.data = collections.defaultdict(lambda: collections.defaultdict(dict))

    def create(self, num, model, **model_params):
        if num > 1 or self.eid is not None:
            raise RuntimeError("Can only create one monitor!")

        self.eid = "Monitor"
        return [{"eid": self.eid, "type": model}]

    def step(self, time, inputs, max_advance):
        data = inputs.get(self.eid, {})
        for key, attrs in data.items():
            for sys, attr in attrs.items():
                self.data[sys][key][time] = attr

        return None

    def finalize(self):
        print("Collected data:")
        for sys, attrs in sorted(self.data.items()):
            print("- %s" % sys)
            for key, values in sorted(attrs.items()):
                print("- %s: %s" % (key, values))


if __name__ == "__main__":
    mosaik_api.start_simulation(Monitor(), "127.0.0.1:5555")

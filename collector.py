"""
a simple data collector, receive any inputs and print them in the end
"""

import mosaik_api

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
        self.data = {}

    def create(self, num, model, **model_params):
        if num > 1 or self.eid is not None:
            raise RuntimeError("Can only create one monitor!")

        self.eid = "Monitor"
        return {"eid": self.eid, "type": model}

    def step(self, time, inputs, max_advance):
        for sys, attrs in inputs.items():
            for key, attr in attrs.items():
                self.data[sys][key][time] = attr

        return None

    def finalize(self):
        print("Collected data:")
        for sys, attrs in self.data.items():
            print("- %s" % sys)
            for key, values in attrs.items():
                print("- %s" % key)
                print("time %s" % values.keys())
                print("attr %s" % values.values())
        return super().finalize()

if __name__ == "__main__":
    mosaik_api.start_simulation(Monitor())
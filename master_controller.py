"""
an master controller for all normal controllers
"""

from mosaik_debug import mosaik_api

META = {
    "type": "event-based",
    "models": {
        "MasterController": {
            "public": True,
            "params": [],
            "attrs": ["delta_in", "delta_out"],
        }
    },
}


class MasterController(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid = "MasterController"
        self.model = None
        self.data = {}
        self.cache = {}

    def create(self, num, model, **model_params):
        if num > 1 or self.model is not None:
            raise Exception(f"Can only instance one {self.eid}!")

        self.model = self.eid
        return [{"eid": self.eid, "type": model}]

    def step(self, time, inputs, max_advance):
        data = {}
        tmp_data = inputs.get(self.eid, {})
        for key, attrs in tmp_data.items():
            if key != "delta_in":
                continue
            for key, attr in attrs.items():
                self.cache[key] = attr

        if sum(self.cache.values()) < -1:
            data[self.eid] = {}
            data[self.eid]["delta_out"] = 0

        self.data = data
        return None

    def get_data(self, outputs):
        data_to_send, self.data = self.data, {}
        return data_to_send

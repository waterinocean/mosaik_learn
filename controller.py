"""
an controller for add model, when val of add model beyond [-3, 3] then change the delta to 1 or -1
"""

import mosaik_api

META = {
    "type": "event-based",
    "models": {
        "Controller": {"public": True, "params": [], "attrs": ["val_in", "delta"]}
    },
}


class Controller(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.entities = {}
        self.eid_prefix = "Controller_"
        self.data = {}

    def create(self, num, model, **model_params):
        if model != "Controller":
            raise Exception(
                f"Can only instance model Controller but give param {model}!"
            )

        next_eid = len(self.entities)
        entities = []
        for i in range(next_eid, next_eid + num):
            eid = f"{self.eid_prefix}{i}"
            self.entities[eid] = eid
            entities.append({"eid": eid, "type": model})

        return entities

    def step(self, time, inputs, max_advance):
        self.data = {}
        for eid, _ in self.entities.items():
            data = inputs.get(eid, {})
            self.data[eid] = {}

            for key, attrs in data.items():
                if key in "delta":
                    if "2" in eid:
                        dd = 1
                    self.data[eid]["delta"] = sum(attrs.values())
                    break

                if key in "val_in":
                    if "2" in eid:
                        dd = 1
                    for _, attr in attrs.items():
                        if attr >= 3:
                            self.data[eid]["delta"] = -1
                        elif attr <= -3:
                            self.data[eid]["delta"] = 1

        return None

    def get_data(self, outputs):
        if self.data:
            data_to_send, self.data = self.data, {}
            return data_to_send

        return None

"""
a simple add operate model, add an delta with an init val and get an output val
"""

from time import time
import mosaik_api

META = {
    "type": "time-based",
    "models": {
        "Model": {
            "public": True,
            "params": ["init_val"],
            "attrs": ["val_out", "delta_in"],
        }
    },
}


class ExampleModel(object):
    def __init__(self, init_val: int = 0) -> None:
        self.init_val = init_val
        self.val = self.init_val
        self.delta = 1

    def step(
        self,
    ):
        self.val += self.delta


class ExampleSim(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = "Model_"
        self.entities = {}

    def create(self, num, model, init_val: int = 0):
        if model != "Model":
            raise Exception("Can only instance model Model!")

        entities = []
        next_eid = len(self.entities)
        for i in range(next_eid, next_eid + num):
            eid = f"{self.eid_prefix}{i}"
            model_instance = ExampleModel(init_val=init_val)
            self.entities[eid] = model_instance
            entities.append({"eid": eid, "type": model})

        return entities

    def step(self, time, inputs, max_advance):
        for model_name, model in self.entities.items():
            data = inputs.get(model_name, {})
            for key, attrs in data.items():
                if key == "delta_in":
                    new_delta = sum(attrs.values())
                    setattr(model, "delta", new_delta)

            model.step()
            print(f"model name: {model_name}, val: {getattr(model, 'val')}")

        return time + 1

    def get_data(self, outputs):
        data_to_send = {}
        for model_name, model in self.entities.items():
            if model_name not in data_to_send:
                data_to_send[model_name] = {}

            val = getattr(model, "val")
            data_to_send[model_name]["val_out"] = val

        return data_to_send


def main():
    mosaik_api.start_simulation(ExampleSim())


if __name__ == "__main__":
    main()

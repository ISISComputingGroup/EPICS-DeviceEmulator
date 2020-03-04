from collections import OrderedDict

import states
from lewis.devices import StateMachineDevice


class SimulatedDMA4500M(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.connected = True
        self.measurement_time = 0

        self.sample_id = 0
        self.target_temperature = 0.0
        self.actual_temperature = 0.0
        self.density = 0.0
        self.condition = "valid"

        self.data_buffer = ""
        self.status = ""

        self.measuring = False
        self.last_measurement_successful = False
        self.setting_temperature = False

    def reset(self):
        self._initialize_data()

    def _get_state_handlers(self):
        return {
            "ready": states.ReadyState(),
            "measuring": states.MeasuringState(),
            "done": states.DoneState(),
        }

    def _get_initial_state(self):
        return "ready"

    def _get_transition_handlers(self):
        return OrderedDict([
            (("ready", "measuring"), lambda: self.measuring is True),
            (("measuring", "ready"), lambda: self.measuring is False and not self.last_measurement_successful),
            (("measuring", "done"), lambda: self.measuring is False and self.last_measurement_successful),
            (("done", "measuring"), lambda: self.measuring is True),
            (("done", "ready"), lambda: self.setting_temperature is True),
            (("ready", "ready"), lambda: self.setting_temperature is True),
        ])

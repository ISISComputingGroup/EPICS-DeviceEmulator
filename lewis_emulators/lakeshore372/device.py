from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedLakeshore372(StateMachineDevice):
    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.temperature = 0
        self.heater_range = 0
        self.heater_power = 0
        self.sensor_resistance = 0
        self.control_mode = 0

        self.p = 0
        self.i = 0
        self.d = 0

        self.connected = True

    def _get_state_handlers(self):
        return {"default": DefaultState()}

    def _get_initial_state(self):
        return "default"

    def _get_transition_handlers(self):
        return OrderedDict([])

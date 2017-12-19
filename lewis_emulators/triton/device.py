from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


SUBSYSTEM_NAMES = {
    "mixing chamber": "mix_chamber_name",
    "heater": "H5"
}


class SimulatedTriton(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.temperature_setpoint = 0
        self.heater_range = 0

        self.heater_power = 1
        self.heater_power_units = "mA"

        self.p = 0
        self.i = 0
        self.d = 0

        self.closed_loop = False

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    def set_p(self, value):
        self.p = value

    def set_i(self, value):
        self.i = value

    def set_d(self, value):
        self.d = value

    def get_p(self):
        return self.p

    def get_i(self):
        return self.i

    def get_d(self):
        return self.d

    def get_temperature_setpoint(self):
        return self.temperature_setpoint

    def set_temperature_setpoint(self, value):
        self.temperature_setpoint = value

    def get_heater_range(self):
        return self.heater_range

    def set_heater_range(self, value):
        self.heater_range = value

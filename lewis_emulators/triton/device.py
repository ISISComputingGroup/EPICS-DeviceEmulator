from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


SUBSYSTEM_NAMES = {
    "mixing chamber": "mix_chamber_name",
    "heater": "H5"
}


class ValveStates(object):
    """
    Enum representing the possible states of a valve.
    """
    OPEN = 0
    CLOSED = 1
    NOT_FOUND = 2


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

        self.valves = [ValveStates.CLOSED] * 10

        self.channels_enabled = [True] * 6

        self.status = "This is a device status message."
        self.automation = "This is the automation status"

    def set_valve_state_backdoor(self, valve, newstate):
        self.valves[int(valve) - 1] = int(newstate)

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

    def get_valve_state(self, valve):
        return self.valves[valve-1]

    def is_channel_enabled(self, chan):
        return self.channels_enabled[chan-1]

    def set_channel_enabled(self, chan, newstate):
        self.channels_enabled[chan-1] = newstate

    def get_status(self):
        return self.status

    def get_automation(self):
        return self.automation

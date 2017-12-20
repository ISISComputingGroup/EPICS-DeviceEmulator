from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


SUBSYSTEM_NAMES = {
    "mixing chamber": "T5",
    "stil": "T1",
    "sorb": "T9",
    "heater": "H5",
    "4khx": "T3",
    "jthx": "T2"
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

        self.stil_temp = 0
        self.mc_temp = 0
        self.sorb_temp = 0
        self.fkhx_temp = 0
        self.jthx_temp = 0

        self.pressures = [0] * 5

    def set_valve_state_backdoor(self, valve, newstate):
        self.valves[int(valve) - 1] = int(newstate)

    def set_pressure_backdoor(self, valve, newpressure):
        self.pressures[int(valve) - 1] = float(newpressure)

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

    def get_stil_temp(self):
        return self.stil_temp

    def get_mc_temp(self):
        return self.mc_temp

    def get_sorb_temp(self):
        return self.sorb_temp

    def get_4khx_temp(self):
        return self.fkhx_temp

    def get_jthx_temp(self):
        return self.jthx_temp

    def get_pressure(self, sensor):
        return self.pressures[sensor]

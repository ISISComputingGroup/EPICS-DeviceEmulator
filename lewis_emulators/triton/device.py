from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


SUBSYSTEM_NAMES = {
    "mixing chamber": "T5",
    "stil": "T1",
    "sorb": "T9",
    "heater": "H5",
    "fkhx": "T3",
    "jthx": "T2",
}


class ValveStates(object):
    """
    Enum representing the possible states of a valve.
    """
    OPEN = 0
    CLOSED = 1
    NOT_FOUND = 2


class TemperatureStage(object):
    def __init__(self, name):
        self.name = name
        self.temperature = 0
        self.enabled = True

        self.p = 0
        self.i = 0
        self.d = 0


class PressureSensor(object):
    def __init__(self):
        self.pressure = 0


class SimulatedTriton(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.temperature_setpoint = 0
        self.heater_range = 0

        self.heater_power = 1
        self.heater_power_units = "mA"

        self.closed_loop = False

        self.valves = [ValveStates.CLOSED] * 10

        self.channels_enabled = [True] * 6

        self.status = "This is a device status message."
        self.automation = "This is the automation status"

        self.pressure_sensors = {"P{}".format(idx): PressureSensor() for idx in range(1, 6)}

        self.temperature_stages = {
            "T1": TemperatureStage("stil"),
            "T2": TemperatureStage("jthx"),
            "T3": TemperatureStage("4khx"),
            "T4": TemperatureStage("sorb"),
            "T5": TemperatureStage("mc"),
        }

    def find_temperature_channel(self, name):
        for k, v in self.temperature_stages.items():
            if v.name == name:
                return k
        else:
            raise ValueError("{} not found".format(name))

    def set_temperature_backdoor(self, stage_name, new_temp):
        self.temperature_stages[self.find_temperature_channel(stage_name)].temperature = new_temp

    def set_valve_state_backdoor(self, valve, newstate):
        self.valves[int(valve) - 1] = int(newstate)

    def set_pressure_backdoor(self, sensor, newpressure):
        self.pressure_sensors["P{}".format(sensor)].pressure = float(newpressure)

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    def get_closed_loop_mode(self):
        return self.closed_loop

    def set_closed_loop_mode(self, mode):
        self.closed_loop = mode

    def set_p(self, stage, value):
        self.temperature_stages[stage].p = value

    def set_i(self, stage, value):
        self.temperature_stages[stage].i = value

    def set_d(self, stage, value):
        self.temperature_stages[stage].d = value

    def get_p(self, stage):
        return self.temperature_stages[stage].p

    def get_i(self, stage):
        return self.temperature_stages[stage].i

    def get_d(self, stage):
        return self.temperature_stages[stage].d

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

    def get_pressure(self, sensor):
        return self.pressure_sensors[sensor].pressure

    def get_temp(self, stage):
        return self.temperature_stages[stage].temperature

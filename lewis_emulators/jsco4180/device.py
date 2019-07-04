import time
from collections import OrderedDict
from states import PumpOff, PumpOn, PumpTimed
from lewis.devices import StateMachineDevice


class SimulatedJsco4180(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.connected = True
        self.single_channel_mode = False

        self.flowrate_sp = 0.010
        self.flowrate = 0.000
        self.pressure = 0
        self.pressure_max = 400
        self.pressure_min = 1

        # Composition components A, B, C, D
        self.component_A = 100.0
        self.component_B = 0.0
        self.component_C = 0.0
        self.component_D = 0.0

        self.pump_mode = "Off"

        self.program_runtime = 0

        self.error = 0
        self.input_correct = True

    @property
    def state(self):
        return self._csm.state

    def crash_pump(self):
        self.device.connected = False

    def _get_state_handlers(self):
        return {
            'pump_off': PumpOff(),
            'pump_on': PumpOn(),
            'pump_timed': PumpTimed(),
        }

    def _get_initial_state(self):
        return 'pump_off'

    def _get_transition_handlers(self):
        return OrderedDict([
            (('pump_on', 'pump_off'), lambda: self.pump_mode == "Off"),
            (('pump_timed', 'pump_off'), lambda: self.pump_mode == "Off"),
            (('pump_off', 'pump_on'), lambda: self.pump_mode == "On"),
            (('pump_off', 'pump_timed'), lambda: self.pump_mode == "Timed")
        ])

    def reset(self):
        self._initialize_data()

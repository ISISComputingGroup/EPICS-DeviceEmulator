from collections import OrderedDict

from lewis.core.statemachine import State
from lewis.devices import StateMachineDevice


class SimulatedSkfMb350Chopper(StateMachineDevice):
    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        self._started = False
        self.phase = 0
        self.frequency = 0
        self.phase_percent_ok = 100.
        self.phase_repeatability = 100.

        self.interlocks = OrderedDict([
            ("DSP_WD_FAIL", False),
            ("OSCILLATOR_FAIL", False),
            ("POSITION_SHUTDOWN", False),
            ("EMERGENCY_STOP", False),
            ("UPS_FAIL", False),
            ("EXTERNAL_FAULT", False),
            ("CC_WD_FAIL", False),
            ("OVERSPEED_TRIP", False),
            ("VACUUM_FAIL", False),
            ("MOTOR_OVER_TEMP", False),
            ("REFERENCE_SIGNAL_LOSS", False),
            ("SPEED_SENSOR_LOSS", False),
            ("COOLING_LOSS", False),
            ("DSP_SUMMARY_SHUTDOWN", False),
            ("CC_SHUTDOWN_REQ", False),
            ("TEST_MODE", False),
        ])

    def set_interlock_state(self, item, value):
        self.interlocks[item] = value

    def get_interlocks(self):
        return self.interlocks

    def _get_state_handlers(self):
        return {
            'init': State(),
        }

    def _get_initial_state(self):
        return 'init'

    def _get_transition_handlers(self):
        return OrderedDict([
            (('init', 'stopped'), lambda: False),
        ])

    def set_frequency(self, frequency):
        self.frequency = frequency

    def get_frequency(self):
        return self.frequency

    def set_nominal_phase(self, phase):
        self.phase = phase

    def set_nominal_phase_window(self, address, phase_window):
        pass

    def start(self):
        self._started = True

    def stop(self):
        self._started = False

    def get_phase(self):
        return self.phase

    def get_phase_percent_ok(self):
        return self.phase_percent_ok

    def get_phase_repeatability(self):
        return self.phase_repeatability

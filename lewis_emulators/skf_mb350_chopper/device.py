from collections import OrderedDict

from lewis.core.statemachine import State
from lewis.devices import StateMachineDevice


class SimulatedSkfMb350Chopper(StateMachineDevice):
    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        # Chopper is only simulated for this one address.
        self.ADDRESS = 1

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
            ("EXTERNAL_FAULT ", False),
            ("CC_WD_FAIL", False),
            ("OVERSPEED_TRIP", False),
            ("VACUUM_FAIL", False),
            ("MOTOR_OVER_TEMP", False),
            ("REFERENCE_SIGNAL_LOSS ", False),
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

    def check_address(self, address):
        if address != self.ADDRESS:
            raise NotImplementedError("Only address 1 is implemented")

    def set_frequency(self, address, frequency):
        self.check_address(address)
        self.frequency = frequency

    def get_frequency(self, address):
        self.check_address(address)
        return self.frequency

    def set_nominal_phase(self, address, phase):
        self.check_address(address)
        self.phase = phase

    def set_nominal_phase_window(self, address, phase_window):
        pass

    def start(self, address):
        self.check_address(address)
        self._started = True

    def stop(self, address):
        self.check_address(address)
        self._started = False

    def get_phase(self, address):
        self.check_address(address)
        return self.phase

    def get_phase_percent_ok(self, address):
        self.check_address(address)
        return self.phase_percent_ok

    def get_phase_repeatability(self, address):
        self.check_address(address)
        return self.phase_repeatability

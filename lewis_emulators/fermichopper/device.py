from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedFermichopper(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.last_command = "0000"
        self.speed_setpoint = 0
        self._allowed_speed_setpoints = (50*i for i in range(1, 13))

        self.delay_highword = 0
        self.delay_lowword = 0
        self.delay = 0

        self.gatewidth = 0

        self.electronics_temp = 30.0
        self.motor_temp = 30.0

        self.voltage = 0
        self.current = 0

        self.autozero_1_lower = 0
        self.autozero_2_lower = 0
        self.autozero_1_upper = 0
        self.autozero_2_upper = 0

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])

    def set_last_command(self, value):
        self.last_command = value

    def get_last_command(self):
        return self.last_command

    def set_speed(self, value):
        assert value in self._allowed_speed_setpoints
        self.speed_setpoint = value

    def get_speed_setpoint(self):
        return self.speed_setpoint

    def get_speed(self):
        # TODO - gradually ramp to speed?
        return self.speed_setpoint

    def set_delay_highword(self, value):
        self.delay_highword = value
        self.update_delay()

    def set_delay_lowword(self, value):
        self.delay_lowword = value
        self.update_delay()

    def update_delay(self):
        self.delay = (self.delay_highword * 65536 + self.delay_lowword)/50400.0

    def set_gate_width(self, value):
        self.gatewidth = value

    def get_gate_width(self):
        return self.gatewidth

    def get_electronics_temp(self):
        return self.electronics_temp

    def get_motor_temp(self):
        return self.motor_temp

    def get_voltage(self):
        return self.voltage

    def get_current(self):
        return self.current

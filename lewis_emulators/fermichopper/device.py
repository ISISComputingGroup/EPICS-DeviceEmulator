from collections import OrderedDict
from states import DefaultState, GoingState, BrokenState, StoppedState, StoppingState
from lewis.devices import StateMachineDevice


class SimulatedFermichopper(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.last_command = "0000"
        self.speed = 0
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

        self.drive = False
        self.runmode = False
        self.magneticbearing = False

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
            'stopping': StoppingState(),
            'going': GoingState(),
            'stopped': StoppedState(),
            'broken': BrokenState()
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
            (('default', 'stopped'), lambda: not self.runmode),
            (('default', 'going'), lambda: self.runmode),
            (('stopped', 'going'), lambda: self.runmode),
            (('going', 'broken'), lambda: self.speed > 10 and not self.magneticbearing),
            (('going', 'stopping'), lambda: self.runmode is False),
            (('stopping', 'stopped'), lambda: self.speed == 0),
            (('stopping', 'broken'), lambda: self.speed > 10 and not self.magneticbearing),
        ])

    def do_command(self, command):
        self.last_command = command

        if command == "0001":
            self.drive = True
            self.runmode = False
        elif command == "0002":
            self.drive = False
        elif command == "0003":
            self.drive = True
            self.runmode = True
        elif command == "0004":
            self.magneticbearing = True
        elif command == "0005":
            self.magneticbearing = False

    def get_last_command(self):
        return self.last_command

    def set_speed_setpoint(self, value):
        assert value in self._allowed_speed_setpoints
        self.speed_setpoint = value

    def get_speed_setpoint(self):
        return self.speed_setpoint

    def set_true_speed(self, value):
        self.speed = value

    def get_true_speed(self):
        return self.speed

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

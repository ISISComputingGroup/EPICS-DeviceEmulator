from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedIndfurn(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.setpoint = 20
        self.pipe_temperature = 25.1
        self.capacitor_bank_temperature = 30.3
        self.fet_temperature = 35.8

        self.p, self.i, self.d = 0, 0, 0
        self.sample_time = 100

        self.direction_heating = True

        self.pid_lower_limit, self.pid_upper_limit = 0, 0

        self.pid_mode_automatic = True
        self.running = True

        self.psu_voltage, self.psu_current, self.output = 0, 0, 0

        self.remote_mode = True
        self.power_supply_on = True
        self.power_supply_fan_on = True
        self.hf_on = False

        self.psu_overtemp, self.psu_overvolt = False, False
        self.cooling_water_flow = True

    def _get_state_handlers(self):
        return {'default': DefaultState()}

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])

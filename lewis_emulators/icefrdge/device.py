from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedIceFridge(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self._auto_temp_setpoint = 0
        self._manual_temp_setpoint = 0
        self.vti_temp1 = 0
        self.vti_temp2 = 0
        self.vti_temp3 = 0
        self.vti_temp4 = 0

    @property
    def auto_temp_setpoint(self):
        return self._auto_temp_setpoint

    @auto_temp_setpoint.setter
    def auto_temp_setpoint(self, new_temp_setpoint):
        self._auto_temp_setpoint = new_temp_setpoint

    @property
    def manual_temp_setpoint(self):
        return self._manual_temp_setpoint

    @manual_temp_setpoint.setter
    def manual_temp_setpoint(self, new_temp_setpoint):
        self._manual_temp_setpoint = new_temp_setpoint

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

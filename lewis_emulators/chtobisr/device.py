from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedChtobisr(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        self.id = "Coherent OBIS Laser Remote - EMULATOR"
        self.status = 00000000
        self.faults = 00000000
        self.interlock = "OFF"

        self.connected = True

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedFinsPLC(StateMachineDevice):

    HELIUM_RECOVERY_NODE = 58

    HE_RECOVERY_MEMORY_FIELD_MAPPING = {
        19500: 'heartbeat',
        19533: 'helium_purity',
        19534: 'dew_point',
    }

    HE_RECOVERY_DOUBLE_WORD_MEMORY_LOCATIONS = {}

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        self.network_address = 0x00
        self.unit_address = 0x00

        self.connected = True

        self.heartbeat = 0
        self.helium_purity = 0
        self.dew_point = 0

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    def reset(self):
        """
        Public method that re-initializes the device's fields.
        :return: Nothing.
        """
        self._initialize_data()

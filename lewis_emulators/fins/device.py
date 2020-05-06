from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedFinsPLC(StateMachineDevice):

    FINS_HE_RECOVERY_NODE = 58

    memory_value_mapping = {
        19500: 1,  # heartbeat
        19533: 999,  # helium purity
        19534: 2136,  # dew point
        19900: 245  # HE_BAG_PR_BE_ATM
    }

    double_word_memory_locations = {}

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        self.network_address = 0x00
        self.unit_address = 0x00

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

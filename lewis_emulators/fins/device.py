from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedFinsPLC(StateMachineDevice):

    HELIUM_RECOVERY_NODE = 58

    HE_RECOVERY_DOUBLE_WORD_MEMORY_LOCATIONS = {}

    PV_NAME_TO_MEMORY_MAPPING = {
        "HEARTBEAT": 19500,
        "HE_PURITY": 19533,
        "DEW_POINT": 19534
    }

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        self.network_address = 0x00
        self.unit_address = 0x00

        self.connected = True

        self.memory = {
            19500: 0,  # heartbeat
            19533: 0,  # helium purity
            19534: 0,  # dew point
        }

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

    def set_memory(self, pv_name, data):
        memory_location = SimulatedFinsPLC.PV_NAME_TO_MEMORY_MAPPING[pv_name]
        self.memory[memory_location] = data

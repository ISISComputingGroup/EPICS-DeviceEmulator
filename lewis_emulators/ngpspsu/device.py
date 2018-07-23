from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedNgpspsu(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.__model_no_and_firmware = "NGPS 100-50:0.9.01"

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    @property
    def model_number_and_firmware(self):
        """
        Returns the model number and firmware version.
        """

        return self.__model_no_and_firmware

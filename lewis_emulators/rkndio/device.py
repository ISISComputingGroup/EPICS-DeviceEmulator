from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedRkndio(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self._idn = "RIKENFE Prototype v2.0"
        self._connected = True
        self.status = "No Error"
        self.error = "No Error"

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
    def idn(self):
        """
        Returns the IDN of the device.

        Returns:
            (string): The IDN of the device.
        """
        return self._idn

    @property
    def connected(self):
        return self._connected

    def connect(self):
        """
        Connects the device.

        Returns:
            None
        """
        self._connected = True

    def disconnect(self):
        """
        Disconnects the device.

        Returns:
            Nome
        """
        self._connected = False


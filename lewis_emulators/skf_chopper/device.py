from collections import OrderedDict

from lewis.devices import StateMachineDevice
from .states import DefaultState


class SimulatedSKFChopper(StateMachineDevice):
    """
    Simulated Eurotherm temperature sensor.
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self.connected = True

        self.state = 0
        self.shaft_angle = 0
        self._address = "A1"
        self.speed = 0
        self.freq = 40 
        self.phasens = 4000
        self.send_ok_transid = True


    def _get_state_handlers(self):
        """
        Returns: states and their names
        """
        return {
            DefaultState.NAME: DefaultState()
        }

    def _get_initial_state(self):
        """
        Returns: the name of the initial state
        """
        return DefaultState.NAME

    def _get_transition_handlers(self):
        """
        Returns: the state transitions
        """
        return OrderedDict()

    @property
    def address(self):
        """
        Get the address of the device.

        Returns: the address of the device e.g. "A01"
        """
        return self._address

    @address.setter
    def address(self, addr):
        """
        Sets the address of the device.

        Args:
            addr (str): the address of this device e.g. "A01".

        """
        self._address = addr

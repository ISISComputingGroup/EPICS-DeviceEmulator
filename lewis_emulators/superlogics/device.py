from collections import OrderedDict

from lewis.devices import StateMachineDevice
from .states import DefaultState


class SimulatedSuperlogics(StateMachineDevice):
    """
    Simulated Superlogics 8019R
    """

    def _initialize_data(self):

        """

        Sets the initial state of the device

        """

        self._values = [0.]*8
        self._version = "A1.0"

    def _get_state_handlers(self):

        """

        Returns: states and their names

        """
        return {
            DefaultState.NAME: DefaultState(),
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

        return OrderedDict([
        ])

    @property
    def values(self):
        """
        :return: All values on this channel
        """
        return self._values

    @values.setter
    def values(self, values):
        """
        :param values: set all the values on this channel
        """
        self._values = values

    @property
    def version(self):
        """
        :return: The firmware version of the device
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Set the firmware version of this device
        :param version: the firmware version as a string
        """
        self._version = version

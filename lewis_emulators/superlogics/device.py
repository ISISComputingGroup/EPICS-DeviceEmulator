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

        self._connected = True
        self._values_1 = [0.]*8
        self._values_2 = [0.]*8
        self._version_1 = "A1.0"
        self._version_2 = "A1.0"

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
    def values_1(self):
        """
        :return: All values on this address
        """
        return self._values_1

    @values_1.setter
    def values_1(self, values):
        """
        :param values: set all the values on this address
        """
        self._values_1 = values

    @property
    def values_2(self):
        """
        :return: All values on this address
        """
        return self._values_2

    @values_2.setter
    def values_2(self, values):
        """
        :param values: set all the values on this address
        """
        self._values_2 = values

    @property
    def version_1(self):
        """
        :return: The firmware version of address 1 of the device
        """
        return self._version_1

    @version_1.setter
    def version_1(self, version):
        """
        Set the firmware version of address 1 this device
        :param version: the firmware version of address 1 as a string
        """
        self._version_1 = version

    @property
    def version_2(self):
        """
        :return: The firmware version of address 2 of the device
        """
        print(self._version_2)
        return self._version_2

    @version_2.setter
    def version_2(self, version):
        """
        Set the firmware version on address 2 of this device
        :param version: the firmware version as a string
        """
        print(version)
        self._version_2 = version

    @property
    def connected(self):
        """
        Get if the current device is in a "disconnected" state
        :return: bool for if the device is disconnected
        """
        return self._connected

    @connected.setter
    def connected(self, value):
        """
        Set if the device is disconnected (for testing purposes)
        :param value: bool to set whether the device is disconnected
        """
        self._connected = value

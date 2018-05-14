from collections import OrderedDict

from lewis.devices import StateMachineDevice
from .states import DefaultState


class FieldUnits(object):
    """
    Field units.
    """
    OERSTED = object()
    GAUSS = object()
    TESLA = object()


class SimulatedDanfysik(StateMachineDevice):
    """
    Simulated Danfysik.
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self.field = 0
        self.field_sp = 0

        self.current = 0
        self.voltage = 0

        self.field_units = FieldUnits.GAUSS
        self.negative_polarity = False
        self.power = True

        # Use a list of active interlocks because each danfysik has different sets of interlocks which can be enabled.
        self.active_interlocks = []

    def enable_interlock(self, name):
        """
        Adds an interlock to the list of enabled interlock
        Args:
            name: the name of the interlock to enable.
        """
        if name not in self.active_interlocks:
            self.active_interlocks.append(name)

    def disable_interlock(self, name):
        """
        Removes an interlock from the list of enabled interlocks
        Args:
            name: the name of the interlock to disable.
        """
        if name in self.active_interlocks:
            self.active_interlocks.remove(name)

    def reset(self):
        """
        Reset the device state.
        """
        self._initialize_data()

    def _get_state_handlers(self):
        """
        Returns: states and their names
        """
        return {DefaultState.NAME: DefaultState()}

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

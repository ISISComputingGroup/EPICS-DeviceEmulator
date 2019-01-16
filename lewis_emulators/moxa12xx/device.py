from collections import OrderedDict
from lewis.devices import StateMachineDevice
from states import DefaultState
from lewis.core.logging import has_log


@has_log
class SimulatedMoxa1210(StateMachineDevice):
    """
    Simulated Moxa ioLogik E1210 Remote I/O device.
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device
        """

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

    def get_di(self, addr, count):
        """
        Gets values from a register on the modbus interface

        Args:
            addr: Integer, the starting address of the values to be retrieved
            count: Integer, the number of contiguous values to get from the modbus register

        Returns:
            Array of values with length count

        """
        return self.interface.di.get(addr, count)

    def set_di(self, addr, value):
        """
        Sets values in the register on the modbus interface

        Args:
            addr: Integer, starting address of the values to be set
            value: List, Containing the data to be written to the register

        Returns:
            None
        """
        self.interface.di.set(addr, value)

    def set_ir(self, addr, value):
        """
        Sets floating point values to the input registers.
        Args:
            addr: Integer, starting address of the values to be set
            value: List, containing the values to be written to the register

        Returns:
            None

        """
        self.interface.ir.set(addr, value)

    def get_ir(self, addr, count):
        """
        Sets floating point values to the input registers.
        Args:
            addr: Integer, starting address of the values to be set
            count: Integer, the number of contiguous values to get from the modbus register

        Returns:
            None

        """
        self.interface.ir.get(addr, count)

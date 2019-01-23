from collections import OrderedDict
from lewis.devices import StateMachineDevice
from states import DefaultState
from lewis.core.logging import has_log

import struct

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
        Set value(s) on the input registers.
        Args:
            addr: Integer, starting address of the values to be set
            value: List, containing the values to be written to the register

        Returns:
            None

        """
        self.interface.ir.set(addr, value)

    def get_ir(self, addr, count):
        """
        Get value(s) from the input registers.
        Args:
            addr: Integer, starting address of the values to be set
            count: Integer, the number of contiguous values to get from the modbus register

        Returns:
            None

        """
        self.interface.ir.get(addr, count)

    def set_1240_voltage(self, addr, value):
        """
        Writes to an input register data a voltage encoded like a moxa e1240 voltage/current logger

        The voltage range for an e1240 is a 0 - 10 V. This is linearly encoded in a 16-bit int, so 0=0V and 2**16=10V

        Args:
            addr: Integer, The address to write the value to
            value: Float, The desired voltage to be written to the input register

        Returns:

        """

        if value > 10.0:
            raw_val = 2**16
        elif value < 0.0:
            raw_val = 0
        else:
            raw_val = int(float(value) * 2**16 / 10.0)

        self.interface.ir.set(addr, (raw_val, ))

    def set_value_on_device(self, addr, value):
        """
        Sets a floating point value to an input register

        Args:
            addr: Integer, the address of the register to be written to
            value: Float, the value to be written.

        Returns:
            None

        """

        integer_representation = struct.unpack('>HH', struct.pack('<f', value))

        self.interface.ir.set(addr, integer_representation)

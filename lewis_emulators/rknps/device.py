from collections import OrderedDict

from lewis.core.logging import has_log
from lewis.devices import StateMachineDevice
from .states import DefaultState


class PowerSupply(object):
    """
    Class representing a single power supply within a chain.
    """
    def __init__(self):
        self.curr = 0
        self.curr_setpoint = 0
        self.volt = 0
        self.is_in_remote_mode = True
        self.pol_positive = True
        self.power_on = True
        self.interlock_active = True


ADDRESSES = ["001", "002"]


@has_log
class SimulatedRknps(StateMachineDevice):
    """
    Simulated Danfysik type controller used in multi-drop mode on RIKEN beamlines.
    """

    def _initialize_data(self):

        self._address = ADDRESSES[0]  # Default to first address.

        self._psus = {}
        for address in ADDRESSES:
            self._psus[address] = PowerSupply()

    def _get_state_handlers(self):
        """
        Returns: states and their names.
        """
        return {DefaultState.NAME: DefaultState()}

    def _get_initial_state(self):
        """
        Returns: the name of the initial state.
        """
        return DefaultState.NAME

    def _get_transition_handlers(self):
        """
        Returns: the state transitions.
        """
        return OrderedDict()

    def get_adr(self):
        """
        Gets the most recently assigned address.

        Returns: a string address.
        """
        return self._address

    def set_adr(self, address):
        """
        Assign a new address. This is how the driver accesses different power supplies on the chain.
        """
        if address not in ADDRESSES:
            raise ValueError("Can not switch to that address - not in known addresses")
        self._address = address

    def _currently_addressed_psu(self):
        """
        Gets the currently addressed power supply

        Returns (PowerSupply) the currently addressed power supply
        """
        return self._psus[self._address]

    def get_current(self):
        """
        Gets the actual value of the output current for the currently addressed power supply.

        Returns: the current
        """
        return self._currently_addressed_psu().curr

    def get_voltage(self):
        """
        Gets the voltage of the currently addressed power supply.

        Returns: the voltage
        """
        return self._currently_addressed_psu().volt

    def is_in_remote_mode(self):
        """
        Gets whether the currently addressed power supply is in remote mode

        Returns: True if the power supply is in remote mode, False otherwise
        """
        return self._currently_addressed_psu().is_in_remote_mode

    def set_in_remote_mode(self, in_remote):
        """
        Sets the control mode of the currently addressed supply.

        Args:
            in_remote: True to set to remote mode, False otherwise
        """

    def is_polarity_positive(self):
        """
        Gets the value of the polarity of the currently addressed power supply.

        Returns: True if the polarity is positive, False otherwise
        """
        return self._currently_addressed_psu().pol_positive

    def set_polarity(self, is_polarity_positive):
        """
        Sets the polarity of the currently addressed power supply

        Args:
            is_polarity_positive: True to set positive polarity, False to set negative polarity
        """
        self._currently_addressed_psu().pol_positive = is_polarity_positive

    def is_power_on(self):
        """
        Gets whether the currently addressed power supply is ON or OFF

        Returns: True if the power supply is on, False otherwise
        """
        return self._currently_addressed_psu().power_on

    def is_interlock_active(self):
        """
        Gets whether the currently addressed power supply's interlock is active

        Returns: True if the interlock is active, False otherwise
        """
        return self._currently_addressed_psu().interlock_active

    def set_power(self, power):
        """
        Call the appropriate routine for on or off.

        Args:
            power: True to turn power on, False to turn power off
        """
        self._currently_addressed_psu().power_on = power

    def set_interlock(self, ilk):
        """
        Set whether the interlocks are active or not.

        This is a backdoor routine, and not accessed from the IOC.

        Args:
            ilk: True to activate interlocks, False to deactivate
        """
        self._currently_addressed_psu().interlock_active = ilk
        if ilk:
            self.set_power(False)

    def set_all_interlocks(self, ilk):
        """
        Set the interlocks of ALL power supplies. This is only ever called via the lewis backdoor.

        Args:
            ilk: True to activate interlocks, False to deactivate
        """
        for address in ADDRESSES:
            self._psus[address].interlock_active = ilk

    def set_all_volt_values(self, val):
        """
        Set the voltages of ALL power supplies. This is only ever called via the lewis backdoor.

        Args:
            val: The value to set the voltages to.
        """
        for address in ADDRESSES:
            self._psus[address].volt = float(val)

    def set_current(self, current):
        """
        Update the values of the information relating to the current.

        The current is multiplied by a default factor of 1000, this is then divided out here as the readback default is
        1.

        Args:
            current: The current to set
        """
        current_to_use = abs(current / 1000.)

        self.set_polarity(current >= 0)

        self._currently_addressed_psu().curr = current_to_use
        self._currently_addressed_psu().curr_setpoint = current_to_use

        self._currently_addressed_psu().volt = current_to_use  # Assume volt == curr

    def reset(self):
        """
        Reset the device to the standard off configuration.
        """
        self.set_current(0)
        self.set_power(False)

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

        # Interlocks
        self.POLNORM = True
        self.TRANS = True
        self.ILK = True
        self.DCOC = True
        self.DCOL = True
        self.REGMOD = True
        self.PREREG = True
        self.PHAS = True
        self.MPSWATER = True
        self.EARTHLEAK = True
        self.THERMAL = True
        self.MPSTEMP = True
        self.DOOR = True
        self.MAGWATER = True
        self.MAGTEMP = True
        self.MPSREADY = True


ADDRESSES = ["001", "002", "003", "004"]


@has_log
class SimulatedRknps(StateMachineDevice):
    """
    Simulated Danfysik type controller used in multi-drop mode on RIKEN beamlines.
    """
    def _initialize_data(self):

        self.connected = True
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

    def get_TRANS(self, ADDR=None):
        """
        Returns transistor fault interlock

        Args:
            ADDR: String, optional.
            The address of the PSU (e.g. 001). If None (default) the currently addressed PSU is used
        Returns:
            interlock_status: Boolean, the current status of the interlock
        """

        if ADDR is not None:
            self.set_adr(ADDR)

        interlock_status = self._currently_addressed_psu().TRANS

        self.log.info('getting trans value {} PSU {}'.format(interlock_status, self.get_adr()))

        return interlock_status

#    @interlock_TRANS.setter
#    def interlock_TRANS(self, value):
#        """
#        Sets transistor fault interlock
#
#        Args:
#            interlock_status: Boolean, True for interlock triggered
#        Returns:
#            None
#        """
#
#        self.log.info('setting trans to {} on {}'.format(value, self.get_adr()))
#
#        self._currently_addressed_psu().TRANS = value

    def set_TRANS(self, value, ADDR):
        """
        Sets transistor fault interlock for PSU at address ADDR

        Args:
            value: Boolean, True for interlock triggered
            ADDR: String, Address of PSU (e.g. 001)
        Returns:
            None
        """

        self.log.info('setting trans to {} on {}'.format(value, self.get_adr()))
        self.set_adr(ADDR)

        self._currently_addressed_psu().TRANS = value

    def get_DCOC(self, ADDR=None):
        """
        Returns DC overcurrent interlock

        Args:
            ADDR: String, optional.
            The address of the PSU (e.g. 001). If None (default) the currently addressed PSU is used
        Returns:
            interlock_status: Boolean, the current status of the interlock
        """

        if ADDR is not None:
            self.set_adr(ADDR)        

        return self._currently_addressed_psu().DCOC

    def set_DCOC(self, value, ADDR):
        """
        Sets DC overcurrent interlock

        Args:
            value: Boolean, True for interlock triggered
            ADDR: String, Address of PSU (e.g. 001)
        Returns:
            None
        """

        self.set_adr(ADDR)

        self._currently_addressed_psu().DCOC = value

    def get_DCOL(self, ADDR=None):
        """
        Returns DC overload interlock

        Args:
            ADDR: String, optional.
            The address of the PSU (e.g. 001). If None (default) the currently addressed PSU is used
        Returns:
            interlock_status: Boolean, the current status of the interlock
        """

        if ADDR is not None:
            self.set_adr(ADDR)

        return self._currently_addressed_psu().DCOL

    def set_DCOL(self, value, ADDR):
        """
        Sets DC overload interlock

        Args:
            value: Boolean, True for interlock triggered
            ADDR: String, Address of PSU (e.g. 001)
        Returns:
            None
        """

        self.set_adr(ADDR)

        self._currently_addressed_psu().DCOL = value

    def get_REGMOD(self, ADDR=None):
        """
        Returns Regulation mode failure interlock

        Args:
            ADDR: String, optional.
            The address of the PSU (e.g. 001). If None (default) the currently addressed PSU is used
        Returns:
            interlock_status: Boolean, the current status of the interlock
        """

        if ADDR is not None:
            self.set_adr(ADDR)

        return self._currently_addressed_psu().REGMOD

    def set_REGMOD(self, value, ADDR):
        """
        Sets Regulation mode failure interlock

        Args:
            value: Boolean, True for interlock triggered
            ADDR: String, Address of PSU (e.g. 001)
        Returns:
            None
        """

        self.set_adr(ADDR)

        self._currently_addressed_psu().REGMOD = value

    def get_PREREG(self, ADDR=None):
        """
        Returns preregulator interlock

        Args:
            ADDR: String, optional.
            The address of the PSU (e.g. 001). If None (default) the currently addressed PSU is used
        Returns:
            interlock_status: Boolean, the current status of the interlock
        """

        if ADDR is not None:
            self.set_adr(ADDR)

        return self._currently_addressed_psu().PREREG

    def set_PREREG(self, value, ADDR):
        """
        Sets preregulator interlock

        Args:
            value: Boolean, True for interlock triggered
            ADDR: String, Address of PSU (e.g. 001)
        Returns:
            None
        """

        self.set_adr(ADDR)

        self._currently_addressed_psu().PREREG = value

    def get_PHAS(self, ADDR=None):
        """
        Returns Phase failure interlock

        Args:
            ADDR: String, optional.
            The address of the PSU (e.g. 001). If None (default) the currently addressed PSU is used
        Returns:
            interlock_status: Boolean, the current status of the interlock
        """

        if ADDR is not None:
            self.set_adr(ADDR)

        return self._currently_addressed_psu().PHAS

    def set_PHAS(self, value, ADDR):
        """
        Sets phase failure interlock

        Args:
            value: Boolean, True for interlock triggered
            ADDR: String, Address of PSU (e.g. 001)
        Returns:
            None
        """

        self.set_adr(ADDR)

        self._currently_addressed_psu().PHAS = value

    def get_MPSWATER(self, ADDR=None):
        """
        Returns MPS water flow interlock

        Args:
            ADDR: String, optional.
            The address of the PSU (e.g. 001). If None (default) the currently addressed PSU is used
        Returns:
            interlock_status: Boolean, the current status of the interlock
        """

        if ADDR is not None:
            self.set_adr(ADDR)

        return self._currently_addressed_psu().MPSWATER

    def set_MPSWATER(self, value, ADDR):
        """
        Sets MPS water flow interlock

        Args:
            value: Boolean, True for interlock triggered
            ADDR: String, Address of PSU (e.g. 001)
        Returns:
            None
        """

        self.set_adr(ADDR)

        self._currently_addressed_psu().MPSWATER = value

    def get_EARTHLEAK(self, ADDR=None):
        """
        Returns earth leak interlock

        Args:
            ADDR: String, optional.
            The address of the PSU (e.g. 001). If None (default) the currently addressed PSU is used
        Returns:
            interlock_status: Boolean, the current status of the interlock
        """

        if ADDR is not None:
            self.set_adr(ADDR)

        return self._currently_addressed_psu().EARTHLEAK

    def set_EARTHLEAK(self, value, ADDR):
        """
        Sets earth leak interlock

        Args:
            value: Boolean, True for interlock triggered
            ADDR: String, Address of PSU (e.g. 001)
        Returns:
            None
        """

        self.set_adr(ADDR)

        self._currently_addressed_psu().EARTHLEAK = value

    def get_THERMAL(self, ADDR=None):
        """
        Returns Thermal breaker interlock

        Args:
            ADDR: String, optional.
            The address of the PSU (e.g. 001). If None (default) the currently addressed PSU is used
        Returns:
            interlock_status: Boolean, the current status of the interlock
        """

        if ADDR is not None:
            self.set_adr(ADDR)

        return self._currently_addressed_psu().THERMAL

    def set_THERMAL(self, value, ADDR):
        """
        Sets Thermal breaker interlock

        Args:
            value: Boolean, True for interlock triggered
            ADDR: String, Address of PSU (e.g. 001)
        Returns:
            None
        """

        self.set_adr(ADDR)

        self._currently_addressed_psu().THERMAL = value

    def get_MPSTEMP(self, ADDR=None):
        """
        Returns MPS over temperature interlock

        Args:
            ADDR: String, optional.
            The address of the PSU (e.g. 001). If None (default) the currently addressed PSU is used
        Returns:
            interlock_status: Boolean, the current status of the interlock
        """

        if ADDR is not None:
            self.set_adr(ADDR)

        return self._currently_addressed_psu().MPSTEMP

    def set_MPSTEMP(self, value, ADDR):
        """
        Sets MPS over temperature interlock

        Args:
            value: Boolean, True for interlock triggered
            ADDR: String, Address of PSU (e.g. 001)
        Returns:
            None
        """

        self.set_adr(ADDR)

        self._currently_addressed_psu().MPSTEMP = value

    def get_DOOR(self, ADDR=None):
        """
        Returns panic button/door interlock

        Args:
            ADDR: String, optional.
            The address of the PSU (e.g. 001). If None (default) the currently addressed PSU is used
        Returns:
            interlock_status: Boolean, the current status of the interlock
        """

        if ADDR is not None:
            self.set_adr(ADDR)

        return self._currently_addressed_psu().DOOR

    def set_DOOR(self, value, ADDR):
        """
        Sets panic button/door interlock

        Args:
            value: Boolean, True for interlock triggered
            ADDR: String, Address of PSU (e.g. 001)
        Returns:
            None
        """

        self.set_adr(ADDR)

        self._currently_addressed_psu().DOOR = value

    def get_MAGWATER(self, ADDR=None):
        """
        Returns manget water interlock

        Args:
            ADDR: String, optional.
            The address of the PSU (e.g. 001). If None (default) the currently addressed PSU is used
        Returns:
            interlock_status: Boolean, the current status of the interlock
        """

        if ADDR is not None:
            self.set_adr(ADDR)

        return self._currently_addressed_psu().MAGWATER

    def set_MAGWATER(self, value, ADDR):
        """
        Sets manget water interlock

        Args:
            value: Boolean, True for interlock triggered
            ADDR: String, Address of PSU (e.g. 001)
        Returns:
            None
        """

        self.set_adr(ADDR)

        self._currently_addressed_psu().MAGWATER = value

    def get_MAGTEMP(self, ADDR=None):
        """
        Returns magnet temperature interlock

        Args:
            ADDR: String, optional.
            The address of the PSU (e.g. 001). If None (default) the currently addressed PSU is used
        Returns:
            interlock_status: Boolean, the current status of the interlock
        """

        if ADDR is not None:
            self.set_adr(ADDR)

        return self._currently_addressed_psu().MAGTEMP

    def set_MAGTEMP(self, value, ADDR):
        """
        Sets magnet temperature interlock

        Args:
            value: Boolean, True for interlock triggered
            ADDR: String, Address of PSU (e.g. 001)
        Returns:
            None
        """

        self.set_adr(ADDR)

        self._currently_addressed_psu().MAGTEMP = value

    def get_MPSREADY(self, ADDR=None):
        """
        Returns MPS not ready interlock

        Args:
            ADDR: String, optional.
            The address of the PSU (e.g. 001). If None (default) the currently addressed PSU is used
        Returns:
            interlock_status: Boolean, the current status of the interlock
        """

        if ADDR is not None:
            self.set_adr(ADDR)

        return self._currently_addressed_psu().MPSREADY

    def set_MPSREADY(self, value, ADDR):
        """
        Sets MPS not ready interlock

        Args:
            value: Boolean, True for interlock triggered
            ADDR: String, Address of PSU (e.g. 001)
        Returns:
            None
        """

        self.set_adr(ADDR)

        self._currently_addressed_psu().MPSREADY = value

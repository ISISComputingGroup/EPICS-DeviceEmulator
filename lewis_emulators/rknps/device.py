from collections import OrderedDict

from lewis.core.logging import has_log
from lewis.devices import StateMachineDevice
from .states import DefaultState

@has_log
class SimulatedRknps(StateMachineDevice):
    """
    Simulated Danfysik type controller used in multi-drop mode on RIKEN beamlines.
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self._active_adr = "001"
        self._adr = {"001":"001","002":"002"}
        self._ra = {"001":123456,"002":456789}
        self._curr = {"001":123456,"002":456789}
        self._volt = {"001":10,"002":20}
        self._cmd  = {"001":"REM","002":"LOC"}
        self._pol = {"001":"+", "002":"-"}
        self._status = {
            "001":[".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."],
            "002":["!",".",".",".",".",".",".",".",".","!",".",".",".",".",".",".",".",".",".",".",".",".",".","."]}
        self._set_curr = {"001":123456,"002":456789}

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

    @property
    def adr(self):
        """
        Gets the most recently assigned address.

        Returns: a string address.
        """
        return self._adr[self._active_adr]

    @property
    def ra(self):
        """
        Gets the RA for the active address.

        Returns: unsigned absolute value of the current setpoint.
        """
        return self._ra[self._active_adr]

    @property
    def ad_curr(self):
        """
            Gets an AD for the active address.

            Returns: value of the output current.
        """
        return self._curr[self._active_adr]

    @property
    def ad_volt(self):
        """
            Gets an AD for the active address.

            Returns: value of the output voltage.
        """
        return self._volt[self._active_adr]

    @property
    def cmd(self):
        """
        Gets the value of the local/remote status.

        Returns: the LOC/REM status of the device.
        """
        return self._cmd[self._active_adr]

    @property
    def pol(self):
        """
        Gets the value of the polarity.

        Returns: the polarity of the device.
        """
        return self._pol[self._active_adr]

    @property
    def status(self):
        """
        Gets the status.

        The status is a 24 character string, with . and ! relating to the value of the associated item.
        In order to allow for easier alteration of the status, it is stored as a list and joined at this point.

        Returns: the status as a string.
        """
        return ''.join(self._status[self._active_adr])

    def set_power(self, power):
        """
        Call the appropriate routine for on or off.

        Args:
            power: turn the power oN or ofF.
        """
        if power == "F":
            self.off()
        elif power == "N":
            self.on()

    def set_interlock(self, ilk):
        """
        Set whether the interlocks are active or not.

        This is a backdoor routine, and not accessed from the IOC.

        Args:
            ilk: whether the interlocks should be active or inactive.
        """
        if ilk == "active":
            self._status[self._active_adr][9] = "!"
            self.off()
        elif ilk == "inactive":
            self._status[self._active_adr][9] = "."

    def set_both_interlocks(self, ilk):
        """
        Set whether the interlocks are active or not.

        This is a backdoor routine, and not accessed from the IOC.
        This specific version is for use with the IOC test framework.

        Args:
            ilk: whether the interlocks should be active or inactive.
        """
        original_active_address = self._active_adr
        self._active_adr = "001"
        self.set_interlock(ilk)
        self._active_adr = "002"
        self.set_interlock(ilk)
        self._active_adr = original_active_address

    def set_current(self, current):
        """
        Update the values of the information relating to the current.

        The current is multiplied by a default factor of 1000, this is then divided out here as the readback default is
        1.

        Args:
            current: The current to set
        """
        current_to_use = current/1000
        self.set_current_values(current_to_use)
        self._set_curr[self._active_adr] = current_to_use

    def reset(self):
        """
        Reset the device to the standard off configuration.
        """
        current_to_use = 0
        self.set_current_values(current_to_use)
        self.off()

    def on(self):
        """
        Turn the device on.

        Set the currents to the last set value.
        Update the status to on.
        """
        current_to_use = self._set_curr[self._active_adr]
        self.set_current_values(current_to_use)
        self._status[self._active_adr][0] = "."

    def set_current_values(self, current_to_use):
        """
        Set all the appropriate current readback and polarity values to a given value.

        Args:
            current_to_use: The current to be set.
        """
        if current_to_use < 0:
            self._pol[self._active_adr] = "-"
        else:
            self._pol[self._active_adr] = "+"
        self._ra[self._active_adr] = abs(current_to_use)
        self._curr[self._active_adr] = current_to_use
        self._volt[self._active_adr] = current_to_use

    def off(self):
        """
        Turn the device off.
        """
        self.set_current_values(0)
        self._status[self._active_adr][0] = "!"

    @has_log
    def set_both_volt_values(self, volt):
        """
        Update the voltage value of both devices.

        This is used only for testing via the backdoor.

        Args:
            volt: the voltage value to set.
        """
        for PSU in self._volt.keys():
            self.log.info("setting for %s" % PSU)
            self._volt[PSU] = float(volt)

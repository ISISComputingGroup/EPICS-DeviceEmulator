from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder

from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")

ILK_STRING = {True: "!", False: "."}
PWR_STRING = {True: ".", False: "!"}

@has_log
class RknpsStreamInterface(StreamInterface):
    """
    Stream interface for the serial port
    """

    in_terminator = "\r"
    out_terminator = "\n\r"

    commands = {
        CmdBuilder("get_voltage").escape("AD 2").eos().build(),
        CmdBuilder("get_current").escape("AD 8").eos().build(),
        CmdBuilder("set_current").escape("WA ").int().eos().build(),
        CmdBuilder("get_ra").escape("RA").eos().build(),

        CmdBuilder("set_power").arg("F|N").eos().build(),
        CmdBuilder("reset").escape("RS").eos().build(),
        CmdBuilder("get_status").escape("S1").eos().build(),

        CmdBuilder("get_pol").escape("PO").eos().build(),
        CmdBuilder("set_pol").escape("PO ").arg("\+|-").eos().build(),

        CmdBuilder("get_cmd").escape("CMD").eos().build(),
        CmdBuilder("set_cmd").arg("LOC|REM").eos().build(),

        CmdBuilder("get_adr").escape("ADR").eos().build(),
        CmdBuilder("set_adr").escape("ADR ").any().eos().build(),
    }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error.

        Args:
            request: requested string.
            error: problem.
        """
        err = "An error occurred at request '{}': {}".format(request, error)
        print(err)
        self.log.error(err)
        return err

    @if_connected
    def set_adr(self, address):
        """
        Sets the active address.

        Args:
            address: The address to use for the following commands.
        """
        self._device.set_adr(address)

    @if_connected
    def get_adr(self):
        """
        Gets the active address.

        Returns: a string address.
        """
        return "{}".format(self._device.get_adr())

    @if_connected
    def get_ra(self):
        """
        Gets the value for RA.

        Returns: a number in 10e-4 Amps.
        """
        return "{:d}".format(int(self._device.get_current()))

    @if_connected
    def get_voltage(self):
        """
        Gets the voltage of the power supply.
        """
        return "{:d}".format(int(self._device.get_voltage()))

    @if_connected
    def get_current(self):
        """
        Gets the current of the power supply.
        """
        return "{:d}".format(int(self._device.get_current()))

    @if_connected
    def get_cmd(self):
        """
        Check whether the device is in Local/Remote mode.

        Returns: LOC for local mode, REM for remote mode.
        """
        return "REM" if self.device.is_in_remote_mode() else "LOC"

    @if_connected
    def set_cmd(self, cmd):
        """
        Sets the active address to be in local or remote mode.

        Args:
            cmd: The mode to set.
        """
        if cmd == "REM":
            self._device.set_in_remote_mode(True)
        elif cmd == "LOC":
            self._device.set_in_remote_mode(False)
        else:
            raise ValueError("Invalid argument to set_cmd")

    @if_connected
    def get_pol(self):
        """
        Get the polarity of the device.

        Returns: The polarity as +/-.
        """
        return "+" if self._device.is_polarity_positive() else "-"

    @if_connected
    def set_pol(self, pol):
        """
        Set the polarity of the device.

        Args:
            pol: The polarity to set.
        """
        if pol == "+":
            self._device.set_polarity(True)
        elif pol == "-":
            self._device.set_polarity(False)
        else:
            raise ValueError("Invalid argument to set_polarity")

        return pol

    @if_connected
    def get_status(self):
        """
        Get the status of the device.

        Returns: A character string for the status.
        """
        device = self._device

        status = ("{POWER}.!.{SPARE}{SPARE}{SPARE}{SPARE}{TRANS}{ILK}{DCOC}{DCOLOAD}{REGMOD}{PREREG}{PHAS}"
                  "{MPSWATER}{EARTHLEAK}{THERMAL}{MPSTEMP}{DOOR}{MAGWATER}{MAGTEMP}"
                  "{MPSREADY}{SPARE}").format(
                        POWER=PWR_STRING[device.is_power_on()],
                        TRANS=ILK_STRING[device.get_TRANS()],
                        ILK=ILK_STRING[device.is_interlock_active()],
                        DCOC=ILK_STRING[device.get_DCOC()],
                        DCOLOAD=ILK_STRING[device.get_DCOL()],
                        REGMOD=ILK_STRING[device.get_REGMOD()],
                        PREREG=ILK_STRING[device.get_PREREG()],
                        PHAS=ILK_STRING[device.get_PHAS()],
                        MPSWATER=ILK_STRING[device.get_MPSWATER()],
                        EARTHLEAK=ILK_STRING[device.get_EARTHLEAK()],
                        THERMAL=ILK_STRING[device.get_THERMAL()],
                        MPSTEMP=ILK_STRING[device.get_MPSTEMP()],
                        DOOR=ILK_STRING[device.get_DOOR()],
                        MAGWATER=ILK_STRING[device.get_MAGWATER()],
                        MAGTEMP=ILK_STRING[device.get_MAGTEMP()],
                        MPSREADY=ILK_STRING[device.get_MPSREADY()],
                        # The spare interlocks aren't always on/off.
                        # Simulate this by making all of the spares "track" one of the other interlocks.
                        SPARE=ILK_STRING[device.get_DOOR()],
                    )

        return status

    @if_connected
    def set_power(self, power):
        """
        Turn the output power of the PSU on or off.

        Args:
            power: Whether to turn the PSU oN or ofF.
        """
        if power == "N":
            self._device.set_power(True)
            self.log.info('PWR ON')
        elif power == "F":
            self._device.set_power(False)
            self.log.info('PWR OFF')
        else:
            raise ValueError("Invalid argument to set_power")

    @if_connected
    def set_current(self, value):
        """
        Set a value for the appropriate DA.

        Considers only the channel for current.

        Args:
            value: The value to apply.
        """
        self._device.set_current(float(value))

    @if_connected
    def reset(self):
        """
        Reset the device, turn it off and set all values to 0.
        """
        self._device.reset()

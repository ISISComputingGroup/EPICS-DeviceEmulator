from lewis.adapters.stream import StreamInterface, has_log
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")

@has_log
class NgpspsuStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_version").escape("VER").build(),
        CmdBuilder("start").escape("MON").build(),
        CmdBuilder("stop").escape("MOFF").build(),
        CmdBuilder("read_status").escape("MST").build(),
        CmdBuilder("reset").escape("MRESET").build(),
        CmdBuilder("read_voltage").escape("MRV").build(),
        CmdBuilder("set_voltage_setpoint").escape("MWV:").float().build(),
        CmdBuilder("read_voltage_setpoint").escape("MWV:?").build(),
        CmdBuilder("read_current").escape("MRI").build(),
        CmdBuilder("set_current_setpoint").escape("MWI:").float().build(),
        CmdBuilder("read_current_setpoint").escape("MWI:?").build()
    }

    out_terminator = "\r\n"
    in_terminator = "\r"

    def handle_error(self, request, error):
        """
        Prints an error message if a command is not recognised.

        Args:
            request : Request.
            error: The error that has occurred.
        Returns:
            None.
        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

        print("An error occurred at request {}: {}".format(request, error))

    @if_connected
    def get_version(self):
        """
        Returns the model number and firmware of the device

        E.g. "#VER:NGPS 100-50:0.9.01" where "NGPS 100-50" is the model
        number and "0.9.01" is the firmware number.
        """
        return "#VER:{}".format(self._device.model_number_and_firmware)

    @if_connected
    def start(self):
        """
        Turns on the device.

        Returns:
            string: "#AK" if the device is turned on. "#NAK%i" otherwise, where %i is an
                error code.
        """
        return self._device.start_device()

    @if_connected
    def stop(self):
        """
        Turns off the device.

        Returns:
            string: "#AK" if the device is turned on. "#NAK%i" otherwise, where %i is an
                error code.
        """
        return self._device.stop_device()

    @if_connected
    def read_status(self):
        """
        Gets the status of the device

        Returns:
            The status of the device which is composed of 8 hexadecimal digts.
        """
        return "#MST:{}".format(self._device.status)

    @if_connected
    def reset(self):
        """
        Resets the device.

        Returns:
            string: "#AK" if the device is turned on. "#NAK%i" otherwise, where %i is an
                error code.
        """
        self.log.info("Reset function was called")
        self.log.info("The status of the device is {}".format(self._device.status))
        return self._device.reset_device()

    @if_connected
    def read_voltage(self):
        """
        Reads the current voltage from the device

        Returns:
            The status of the device which is composed of 8 hexadecimal digts.
        """
        return "#MRV:{}".format(self._device.voltage)

    @if_connected
    def set_voltage_setpoint(self, value):
        """
        Try's to set the voltage setpoint to value.

        Args:
            value: string of a decimal to 6 decimal places

        Returns:
            "#AK" if successful and "#NAK:%i" if not where %i is an error
                code.
        """
        return self._device.try_setting_voltage_setpoint(value)

    @if_connected
    def read_voltage_setpoint(self):
        """
        Reads the last voltage setpoint from the device.

        Returns:
            string: #MWV:%f" where %f is the last voltage setpoint set.
        """
        return "#MWV:{}".format(self._device.voltage_setpoint)

    @if_connected
    def read_current(self):
        """
        Reads the current voltage from the device

        Returns:
            The status of the device which is composed of 8 hexadecimal digts.
        """
        return "#MRI:{}".format(self._device.current)

    @if_connected
    def set_current_setpoint(self, value):
        """
        Try's to set the voltage setpoint to value.

        Args:
            value: string of a decimal to 6 decimal places

        Returns:
            "#AK" if successful and "#NAK:%i" if not where %i is an error
                code.
        """
        return self._device.try_setting_current_setpoint(value)

    @if_connected
    def read_current_setpoint(self):
        """
        Reads the last voltage setpoint from the device.

        Returns:
            string: #MWV:%f" where %f is the last voltage setpoint set.
        """
        return "#MWI:{}".format(self._device.current_setpoint)

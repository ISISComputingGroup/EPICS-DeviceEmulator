from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder

# Dictionaries for parameter states (strings required to build reply to "all status" command)
OK_NOK = {True: "OK", False: "NOK"}
ON_OFF = {True: "ON", False: "OFF"}
START_STOP = {True: "START", False: "STOP"}
CW_CCW = {True: "CLOCK", False: "ANTICLOCK"}


@has_log
class FZJDDFCHStreamInterface(StreamInterface):
    """
    Stream interface for the Ethernet port
    """

    commands = {
        CmdBuilder("get_magnetic_bearing_status").arg(".{3}").escape("?;MBON?").build(),
        CmdBuilder("get_all_status").arg(".{3}").escape("?;ASTA?").build(),
        CmdBuilder("set_frequency", arg_sep="").arg(".{3}").escape("!;FACT!;").int().build(),
        CmdBuilder("set_phase", arg_sep="").arg(".{3}").escape("!;PHAS!;").float().build(),
        CmdBuilder("set_magnetic_bearing", arg_sep="").arg(".{3}").escape("!;MAGB!;").any().build(),
        CmdBuilder("set_drive_mode", arg_sep="").arg(".{3}").escape("!;DRIV!;").any().build()
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def set_frequency(self, chopper_name, frequency):
        if self._device.disconnected:
            return None
        if self._device.error_on_set_frequency is None:
            self._device.frequency_setpoint = int(frequency) * self._device.frequency_reference
            reply = "{chopper_name}OK".format(chopper_name=chopper_name)
        else:
            reply = "ERROR;{}".format(self._device.error_on_set_frequency)

        self.log.info(reply)
        return reply

    def set_phase(self, chopper_name, phase):
        if self._device.disconnected:
            return None
        if self._device.error_on_set_phase is None:
            self._device.phase_setpoint = float(phase)
            reply = "{chopper_name}OK".format(chopper_name=chopper_name)
        else:
            reply = "ERROR;{}".format(self._device.error_on_set_phase)

        self.log.info(reply)
        return reply

    def set_magnetic_bearing(self, chopper_name, magnetic_bearing):
        if self._device.disconnected:
            return None
        if self._device.error_on_set_magnetic_bearing is None:
            self._device.magnetic_bearing_is_on = ON_OFF.keys()[ON_OFF.values().index(magnetic_bearing)]
            reply = "{chopper_name}OK".format(chopper_name=chopper_name)
        else:
            reply = "ERROR;{}".format(self._device.error_on_set_magnetic_bearing)

        self.log.info(reply)
        return reply

    def set_drive_mode(self, chopper_name, drive_mode):
        if self._device.disconnected:
            return None
        if self._device.error_on_set_drive_mode is None:
            self._device.drive_mode_is_start = START_STOP.keys()[START_STOP.values().index(drive_mode)]
            reply = "{chopper_name}OK".format(chopper_name=chopper_name)
        else:
            reply = "ERROR;{}".format(self._device.error_on_set_drive_mode)

        self.log.info(reply)
        return reply

    def get_magnetic_bearing_status(self, chopper_name):

        """
        Gets the magnetic bearing status for the FZJ Digital Drive Fermi Chopper Controller

        :param
        Returns:

        """
        if self._device.disconnected:
            return None
        device = self._device
        return "{0:3s};MBON?;{}".format(device.chopper_name, self._device.magnetic_bearing_status)

    def get_all_status(self, chopper_name):

        """
        Gets the all status for the FZJ Digital Drive Fermi Chopper Controller

        :param 
        Returns:

        """
        device = self._device
        if self._device.disconnected or chopper_name != device.chopper_name:
            return None

        values = [
            "{0:3s}".format(device.chopper_name),
            "{0:.2f}".format(device.frequency_reference),
            "{0:.2f}".format(device.frequency_setpoint),
            "{0:.2f}".format(device.frequency),
            "{0:.2f}".format(device.phase_setpoint),
            "{0:.2f}".format(device.phase),
            "{0:s}".format(OK_NOK[device.phase_status_is_ok]),
            "{0:s}".format(ON_OFF[device.magnetic_bearing_is_on]),
            "{0:s}".format(OK_NOK[device.magnetic_bearing_status_is_ok]),
            "{0:.1f}".format(device.magnetic_bearing_integrator),
            "{0:s}".format(ON_OFF[device.drive_is_on]),
            "{0:s}".format(START_STOP[device.drive_mode_is_start]),
            "{0:.2f}".format(device.drive_l1_current),
            "{0:.2f}".format(device.drive_l2_current),
            "{0:.2f}".format(device.drive_l3_current),
            "{0:s}".format(CW_CCW[device.drive_direction_is_cw]),
            "{0:s}".format(OK_NOK[device.parked_open_status_is_ok]),
            "{0:.2f}".format(device.drive_temperature),
            "{0:.2f}".format(device.input_clock),
            "{0:.2f}".format(device.phase_outage),
            "{0:3s}".format(device.master_chopper),
            "{0:s}".format(ON_OFF[device.logging_is_on]),
            "{0:s}".format(OK_NOK[device.lmsr_status_is_ok]),
            "{0:s}".format(OK_NOK[device.dsp_status_is_ok]),
            "{0:s}".format(OK_NOK[device.interlock_er_status_is_ok]),
            "{0:s}".format(OK_NOK[device.interlock_vacuum_status_is_ok]),
            "{0:s}".format(OK_NOK[device.interlock_frequency_monitoring_status_is_ok]),
            "{0:s}".format(OK_NOK[device.interlock_magnetic_bearing_amplifier_temperature_status_is_ok]),
            "{0:s}".format(OK_NOK[device.interlock_magnetic_bearing_amplifier_current_status_is_ok]),
            "{0:s}".format(OK_NOK[device.interlock_drive_amplifier_temperature_status_is_ok]),
            "{0:s}".format(OK_NOK[device.interlock_drive_amplifier_current_status_is_ok]),
            "{0:s}".format(OK_NOK[device.interlock_ups_status_is_ok])
        ]

        return_string = ";".join(values)

        # print reply string in log
        # self.log.info(return_string)

        return return_string

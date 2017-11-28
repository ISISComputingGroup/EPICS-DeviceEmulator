from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder


@has_log
class FZJDDFCHStreamInterface(StreamInterface):
    """
    Stream interface for the Ethernet port
    """

    commands = {
        CmdBuilder("get_magnetic_bearing_status").escape("MBON?").build(),
        CmdBuilder("get_all_status").arg(".{3}").escape(";ASTA?").build(),
        CmdBuilder("set_frequency", arg_sep="").arg(".{3}").escape("!;FACT!;").int().build()
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

        if self._device.error_on_set_frequency is None:
            self._device.frequency_setpoint = int(frequency) * self._device.frequency_reference
            reply = "{chopper_name}OK".format(chopper_name=chopper_name)
        else:
            reply = self._device.error_on_set_frequency

        self.log.info(reply)
        return reply

    def get_magnetic_bearing_status(self):

        """
        Gets the magnetic bearing status for the FZJ Digital Drive Fermi Chopper Controller

        :param
        Returns:

        """
        pass

        # return self._device.magnetic_bearing_status
        return

    def get_all_status(self, chopper_name):

        """
        Gets the all status for the FZJ Digital Drive Fermi Chopper Controller

        :param 
        Returns:

        """
        device = self._device
        if chopper_name != device.chopper_name:
            return None
        drive_direction = "CLOCK" if device.is_drive_direction_clockwise else "ANTICLOCK"
        values = [
            "{0:3s}".format(device.chopper_name),
            "{0:.2f}".format(device.frequency_reference),
            "{0:.2f}".format(device.frequency_setpoint),
            "{0:.2f}".format(device.frequency),
            "{0:.2f}".format(device.phase_setpoint),
            "{0:.2f}".format(device.phase),
            "{0:s}".format(device.phase_status),
            "{0:s}".format(device.magnetic_bearing),
            "{0:s}".format(device.magnetic_bearing_status),
            "{0:.1f}".format(device.magnetic_bearing_integrator),
            "{0:s}".format(device.drive),
            "{0:s}".format(device.drive_status),
            "{0:.2f}".format(device.drive_l1_current),
            "{0:.2f}".format(device.drive_l2_current),
            "{0:.2f}".format(device.drive_l3_current),
            "{0:s}".format(drive_direction),
            "{0:s}".format(device.parked_open_status),
            "{0:.2f}".format(device.drive_temperature),
            "{0:.2f}".format(device.input_clock),
            "{0:.2f}".format(device.phase_outage),
            "{0:s}".format(device.master_chopper),
            "{0:s}".format(device.logging),
            "{0:s}".format(device.lmsr_status),
            "{0:s}".format(device.dsp_status),
            "{0:s}".format(device.interlock_er_status),
            "{0:s}".format(device.interlock_vacuum_status),
            "{0:s}".format(device.interlock_frequency_monitoring_status),
            "{0:s}".format(device.interlock_magnetic_bearing_amplifier_temperature_status),
            "{0:s}".format(device.interlock_magnetic_bearing_amplifier_current_status),
            "{0:s}".format(device.interlock_drive_amplifier_temperature_status),
            "{0:s}".format(device.interlock_drive_amplifier_current_status),
            "{0:s}".format(device.interlock_ups_status)
        ]

        return_string = ";".join(values)

        # print reply string in log
        # self.log.info(return_string)

        return return_string

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
        CmdBuilder("get_all_status").escape("ASTA?").build()
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

    def get_magnetic_bearing_status(self):

        """
        Gets the magnetic bearing status for the FZJ Digital Drive Fermi Chopper Controller

        :param
        Returns:

        """
        pass

        # return self._device.magnetic_bearing_status
        return

    def get_all_status(self):

        """
        Gets the all status for the FZJ Digital Drive Fermi Chopper Controller

        :param 
        Returns:

        """
        device = self._device
        values = [
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
            "{0:s}".format(device.drive_direction),
            "{0:s}".format(device.parked_open_status),
            "{0:.2f}".format(device.drive_temperature),
            "{0:.2f}".format(device.input_clock)
        ]

        return_string = ";".join(values)
        self.log.error(return_string)
        return return_string

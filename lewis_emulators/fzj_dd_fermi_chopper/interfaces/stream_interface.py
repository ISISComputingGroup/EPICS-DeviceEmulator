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
        return self._device.magnetic_bearing_status

    def get_all_status(self):

        """
        Gets the all status for the FZJ Digital Drive Fermi Chopper Controller

        :param 
        Returns:

        """
        return "{freq_ref:.2f};{freq_setp:.2f};{freq:.2f};{phas_setp:.2f};{phas:.2f};{phas_stat:s}"\
            .format(freq_ref=self._device.reference_frequency, freq_setp=self._device.frequency_setpoint,
            freq=self._device.frequency, phas_setp=self._device.phase_setpoint, phas=self._device.phase,
            phas_stat=self._device.phase_status)

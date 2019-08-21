from lewis.adapters.stream import StreamInterface, Cmd
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from time import sleep


@has_log
class OerconeStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("enquiry").escape("05").eos().build(),
        CmdBuilder("get_pressure").escape("PR1\r").eos().build(),
        CmdBuilder("get_measurement_unit").escape("UNI\r").eos().build()
    }

    in_terminator = "\n"
    out_terminator = "\n"

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    def setup_channel(self):
        pass

    def enquiry(self):
        pass

    def get_pressure(self):
        # The protocol for talking to the device has to wait 100ms
        sleep(0.1)
        return self._device.pressure

    def get_measurement_unit(self):
        # Wait 100 ms as that is what is in the protocol from the ticket
        sleep(0.1)
        return self._device.measurement_unit.value

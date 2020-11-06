from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder


def _split_command_output(command):
    return command.split(",")


class SmrtmonStreamInterface(StreamInterface):
    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_stat").escape("STAT").build(),
        CmdBuilder("get_oplm").escape("OPLM").build(),
        CmdBuilder("get_lims").escape("LIMS").build(),
    }
    in_terminator = "\r"
    # Out terminator is defined in ResponseBuilder instead as we need to add it to two messages.
    out_terminator = "\r"

    def handle_error(self, request, error):
        print("An error occurred at request " + repr(request) + ": " + repr(error))
        return str(error)

    def get_stat(self):
        return "{},{},{},{},{},{},{},{},{},{},{}".format(self._device.temp1,
                                                         self._device.temp2.stat,
                                                         self._device.temp3.stat,
                                                         self._device.temp4.stat,
                                                         self._device.temp5.stat,
                                                         self._device.temp6.stat,
                                                         self._device.volt1.stat,
                                                         self._device.volt2.stat,
                                                         self._device.volt3.stat,
                                                         self._device.mi,
                                                         self._device.status)

    def get_oplm(self):
        return "{},{},{},{},{},{},{},{},{}".format(self._device.temp1,
                                                   self._device.temp2.oplm,
                                                   self._device.temp3.oplm,
                                                   self._device.temp4.oplm,
                                                   self._device.temp5.oplm,
                                                   self._device.temp6.oplm,
                                                   self._device.volt1.oplm,
                                                   self._device.volt2.oplm,
                                                   self._device.volt3.oplm)

    def get_lims(self):
        return "{},{},{},{},{},{},{},{},{}".format(self._device.temp1,
                                                   self._device.temp2.lims,
                                                   self._device.temp3.lims,
                                                   self._device.temp4.lims,
                                                   self._device.temp5.lims,
                                                   self._device.temp6.lims,
                                                   self._device.volt1.lims,
                                                   self._device.volt2.lims,
                                                   self._device.volt3.lims)

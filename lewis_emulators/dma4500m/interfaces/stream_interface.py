from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")


@has_log
class DMA4500MStreamInterface(StreamInterface):

    in_terminator = "\r"
    out_terminator = "\r"

    # Commands that we expect via serial during normal operation
    def __init__(self):
        super(DMA4500MStreamInterface, self).__init__()
        self.commands = {
            CmdBuilder(self.start).escape("start").eos().build(),
            CmdBuilder(self.abort).escape("abort").eos().build(),
            CmdBuilder(self.finished).escape("finished").eos().build(),
            CmdBuilder(self.set_temperature).escape("set").optional(" ").escape("temperature ").arg(".+").eos().build(),
            CmdBuilder(self.get_data).escape("get").optional(" ").escape("data").eos().build(),
            CmdBuilder(self.get_data_with_subs).escape("get").optional(" ").escape("data").optional(" ").escape("with").optional(" ").escape("subs").eos().build(),
            CmdBuilder(self.get_raw_data).escape("get").optional(" ").escape("raw").optional(" ").escape("data").eos().build(),
        }

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    @if_connected
    def start(self):
        if self._device.measuring:
            return "measurement already started"

        self._device.sample_id += 1
        self._device.measuring = True
        return "measurement started"

    @if_connected
    def abort(self):
        if not self._device.measuring:
            return "measurement not started"

        self._device.measuring = False
        return "measurement aborted"

    @if_connected
    def finished(self):
        print(self._device.status)
        return self._device.status

    @if_connected
    def set_temperature(self, temperature_arg):
        try:
            temperature = float(temperature_arg)
        except ValueError:
            return "the given temperature could not be parsed"

        if self._device.measuring:
            return "not allowed during measurement"

        self._device.target_temperature = temperature
        self._device.setting_temperature = True
        return "accepted"

    @if_connected
    def get_data(self):
        if not self._device.data_buffer:
            return "no new data"

        data = self._device.data_buffer
        print(data)
        self._device.data_buffer = ""
        return data

    @if_connected
    def get_data_with_subs(self):
        return self.get_data()

    @if_connected
    def get_raw_data(self):
        sample_id = self._device.sample_id or "NaN"
        return "{0:.6f};{1:.2f};{2:.2f};{3}".format(self._device.density,
                                                    self._device.actual_temperature,
                                                    self._device.target_temperature,
                                                    sample_id)

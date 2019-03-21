from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder


@has_log
class Lakeshore340StreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_temperature_a").escape("KRDG? 0").eos().build(),
        CmdBuilder("get_temperature_b").escape("KRDG? 1").eos().build(),
        CmdBuilder("get_temperature_c").escape("KRDG? 2").eos().build(),
        CmdBuilder("get_temperature_d").escape("KRDG? 3").eos().build(),

        CmdBuilder("get_measurement_a").escape("SRDG? 0").eos().build(),
        CmdBuilder("get_measurement_b").escape("SRDG? 1").eos().build(),
        CmdBuilder("get_measurement_c").escape("SRDG? 2").eos().build(),
        CmdBuilder("get_measurement_d").escape("SRDG? 3").eos().build(),

        CmdBuilder("set_tset").escape("SETP 1,").float().eos().build(),
        CmdBuilder("get_tset").escape("SETP? 1").eos().build(),

        CmdBuilder("set_pid").escape("PID 1,").float().escape(",").float().escape(",").int().eos().build(),
        CmdBuilder("get_pid").escape("PID? 1").eos().build(),
    }

    in_terminator = "\n"
    out_terminator = "\n"

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    def get_temperature_a(self):
        return self._device.temp_a

    def get_temperature_b(self):
        return self._device.temp_b

    def get_temperature_c(self):
        return self._device.temp_c

    def get_temperature_d(self):
        return self._device.temp_d

    def get_measurement_a(self):
        return self._device.measurement_a

    def get_measurement_b(self):
        return self._device.measurement_b

    def get_measurement_c(self):
        return self._device.measurement_c

    def get_measurement_d(self):
        return self._device.measurement_d

    def set_tset(self, val):
        self._device.tset = float(val)

    def get_tset(self):
        return self._device.tset

    def set_pid(self, p, i, d):
        self._device.p, self._device.i, self._device.d = p, i, d

    def get_pid(self):
        return "{},{},{}".format(self._device.p, self._device.i, self._device.d)
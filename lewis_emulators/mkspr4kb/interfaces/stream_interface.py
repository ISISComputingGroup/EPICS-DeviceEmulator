import functools

import six
from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")


class MKS_PR4000B_StreamInterface(StreamInterface):
    def __init__(self):
        super(MKS_PR4000B_StreamInterface, self).__init__()

        self.commands = {
            CmdBuilder("get_value").escape("AV").int().eos().build(),

            CmdBuilder("get_valve_status").escape("?VL").int().eos().build(),
            CmdBuilder("set_valve_status").escape("VL").int().escape(",").enum("ON", "OFF").eos().build(),

            CmdBuilder("get_relay_status").escape("?RL").int().eos().build(),
            CmdBuilder("set_relay_status").escape("RL").int().escape(",").enum("ON", "OFF").eos().build(),
        }

        # Done like this to avoid excessive code duplication.
        float_get_and_set_commands = {
            "SP": "setpoint",
            "GN": "gain",
            "OF": "offset",
            "RO": "rtd_offset",
            "IN": "input_range",
            "OT": "output_range",
            "EI": "ext_input_range",
            "EO": "ext_output_range",
            "SC": "scale",
            "UL": "upper_limit",
            "LL": "lower_limit",
        }

        # Closures to force the functions to bind correctly (trying to create these in the loop will run into
        # late-binding issues.
        def getter_factory(name):
            def getter(chan):
                if not self.device.connected:
                    return None
                return "{:.2f}".format(getattr(self.device.channels[chan], name))
            return getter

        def setter_factory(name):
            def setter(chan, value):
                if not self.device.connected:
                    return None
                setattr(self.device.channels[chan], name, value)
                return ""
            return setter

        # Update the command mapping with the newly-generated commands.
        for command_name, emulator_name in six.iteritems(float_get_and_set_commands):
            self.commands.update({
                CmdBuilder(setter_factory(emulator_name)).escape(command_name).int().escape(",").float().eos().build(),
                CmdBuilder(getter_factory(emulator_name)).escape("?{}".format(command_name)).int().eos().build(),
            })

    in_terminator = "\r"
    out_terminator = "\r"

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    @if_connected
    def get_value(self, chan):
        return "{:.2f}".format(self.device.channels[chan].setpoint)

    @if_connected
    def get_valve_status(self, chan):
        return "ON" if self.device.channels[chan].valve_enabled else "OFF"

    @if_connected
    def set_valve_status(self, chan, status):
        self.device.channels[chan].valve_enabled = (status == "ON")
        return ""

    @if_connected
    def get_relay_status(self, chan):
        return "ON" if self.device.channels[chan].relay_enabled else "OFF"

    @if_connected
    def set_relay_status(self, chan, status):
        self.device.channels[chan].relay_enabled = (status == "ON")
        return ""


from lewis.adapters.stream import StreamInterface

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply, timed_reply

if_connected = conditional_reply("connected")
if_input_error = conditional_reply("input_correct", "%%[Error:stack underflow]%%")
if_valid_input_delay = timed_reply(action="crash_pump", minimum_time_delay=100)


class Jsco4180StreamInterface(StreamInterface):

    in_terminator = '\r'
    out_terminator = '\r\n'

    def __init__(self):

        super(Jsco4180StreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.set_flowrate).float().escape(" flowrate set").build(),
            CmdBuilder(self.get_flowrate).escape("a_flow load p").eos().build(),
            CmdBuilder(self.get_pressure).escape("a_press1 load p").eos().build(),
            CmdBuilder(self.set_pressure_max).int().escape(" pmax set").build(),
            CmdBuilder(self.get_pressure_max).escape("a_pmax load p").eos().build(),
            CmdBuilder(self.set_pressure_min).int().escape(" pmin set").build(),
            CmdBuilder(self.get_pressure_min).escape("a_pmin load p").eos().build(),
            CmdBuilder(self.get_program_runtime).escape("current_time load p").eos().build(),
            CmdBuilder(self.get_component_a).escape("compa load p").eos().build(),
            CmdBuilder(self.get_component_b).escape("compb load p").eos().build(),
            CmdBuilder(self.get_component_c).escape("compc load p").eos().build(),
            CmdBuilder(self.get_component_d).escape("compd load p").eos().build(),
            CmdBuilder(self.set_composition).float().escape(" ").float().escape(" ").float().escape(" ").float()
                                            .escape(" comp set").build(),
            CmdBuilder(self.get_error).escape("trouble load p").eos().build(),
            CmdBuilder(self.set_error).escape("0 trouble set").build(),
            CmdBuilder(self.set_pump).int().escape(" pump set").eos().build(),
        }

    def catch_all(self):
        pass

    @if_valid_input_delay
    @if_connected
    def set_pump(self, mode):
        if mode == 1:
            # Pump off
            self.device.pump_mode = "Off"
            self.device.flowrate = 0.000
            self.device.pressure = 0
            self.device.program_runtime = 0
            return self.out_terminator
        elif mode == 6:
            # Pump on
            self.device.pump_mode = "On"
            self.device.flowrate = self.device.flowrate_sp
            self.device.pressure = (self.device.pressure_max - self.device.pressure_min) // 2
            return self.out_terminator
        elif mode == 8:
            # Pump timed
            self.device.pump_mode = "Timed"
            self.device.program_runtime = 0
            self.device.flowrate = self.device.flowrate_sp
            self.device.pressure = (self.device.pressure_max - self.device.pressure_min) // 2
            return self.out_terminator
        else:
            # Ignore others
            self.device.pump_mode = "Off"
            return self.out_terminator

    @if_valid_input_delay
    @if_connected
    @if_input_error
    def set_flowrate(self, flowrate):
        self.device.flowrate_sp = flowrate
        return self.out_terminator

    @if_valid_input_delay
    @if_connected
    def get_flowrate(self):
        return self.device.flowrate

    @if_valid_input_delay
    @if_connected
    def get_pressure(self):
        return self.device.pressure

    @if_valid_input_delay
    @if_connected
    def set_pressure_max(self, pressure_max):
        self.device.pressure_max = pressure_max
        return self.out_terminator

    @if_valid_input_delay
    @if_connected
    def get_pressure_max(self):
        return self.device.pressure_max

    @if_valid_input_delay
    @if_connected
    def set_pressure_min(self, pressure_min):
        self.device.pressure_min = pressure_min
        return self.out_terminator

    @if_valid_input_delay
    @if_connected
    def get_pressure_min(self):
        return self.device.pressure_min

    @if_valid_input_delay
    @if_connected
    def get_program_runtime(self):
        if self.device.pump_mode == 'Timed':
            self.device.program_runtime += 1
        return self.device.program_runtime

    @if_valid_input_delay
    @if_connected
    def get_component_a(self):
        if self.device.single_channel_mode:
            result = 100
        else:
            result = self.device.component_A
        return result

    @if_valid_input_delay
    @if_connected
    def get_component_b(self):
        if self.device.single_channel_mode:
            result = 0
        else:
            result = self.device.component_B
        return result

    @if_valid_input_delay
    @if_connected
    def get_component_c(self):
        if self.device.single_channel_mode:
            result = 0
        else:
            result = self.device.component_C
        return result

    @if_valid_input_delay
    @if_connected
    def get_component_d(self):
        if self.device.single_channel_mode:
            result = 0
        else:
            result = self.device.component_D
        return result

    @if_valid_input_delay
    @if_connected
    def set_composition(self, ramptime, a, b, c):
        self.device.component_A = a
        self.device.component_B = b
        self.device.component_C = c
        self.device.component_D = 100 - (a + b + c)
        return self.out_terminator

    @if_valid_input_delay
    @if_connected
    def get_error(self):
        return self.device.error

    @if_valid_input_delay
    @if_connected
    def set_error(self):
        self.device.error = 0
        return self.out_terminator

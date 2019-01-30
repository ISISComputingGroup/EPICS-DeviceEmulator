from lewis.adapters.stream import StreamInterface, Cmd

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply('connected')
if_input_error = conditional_reply('input_correct', "%%[Error:file open error]%%")

class Jsco4180StreamInterface(StreamInterface):

    in_terminator = '\r\n'
    out_terminator = '\r'

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
            CmdBuilder(self.set_pump_off_timer).float().escape(" offtimer set").build(),
            CmdBuilder(self.set_pump_on_timer).float().escape(" ontimer set").build(),
            CmdBuilder(self.set_valve_position).int().escape(" valve set").build(),
            CmdBuilder(self.get_valve_position).escape("valve load p").eos().build(),
            CmdBuilder(self.set_file_number).int().escape(" fileno set").build(),
            CmdBuilder(self.set_file_open).int().escape(" openfile").build(),
            CmdBuilder(self.set_file_close).escape("closefile").build(),
            CmdBuilder(self.get_program_runtime).escape("current_time load p").eos().build(),
            CmdBuilder(self.get_composition_a).escape("compa load p").eos().build(),
            CmdBuilder(self.get_composition_b).escape("compb load p").eos().build(),
            CmdBuilder(self.get_composition_c).escape("compc load p").eos().build(),
            CmdBuilder(self.get_composition_d).escape("compd load p").eos().build(),
            CmdBuilder(self.set_composition).float().escape(" ").float().escape(" ").float().escape(" ").float().escape(" comp set").build(),
            CmdBuilder(self.get_error).escape("trouble load p").eos().build(),
            CmdBuilder(self.set_error).escape("0 trouble set").build(),
            CmdBuilder(self.set_pump).int().escape(" pump set").eos().build(),
        }

    def catch_all(self):
        pass

    @if_connected
    def set_pump(self, mode):
        if mode == 1:
            # Pump off
            self.device.pump_mode = "Off"
            self.device.flowrate = 0.000
            self.device.pressure = 0
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

    @if_connected
    def set_flowrate(self, flowrate):
        self.device.flowrate_sp = flowrate
        return self.out_terminator

    @if_connected
    def get_flowrate(self):
        return self.device.flowrate

    @if_connected
    def get_pressure(self):
        return self.device.pressure

    @if_connected
    def set_pressure_max(self, pressure_max):
        self.device.pressure_max = pressure_max
        return self.out_terminator

    @if_connected
    def get_pressure_max(self):
        return self.device.pressure_max

    @if_connected
    def set_pressure_min(self, pressure_min):
        self.device.pressure_min = pressure_min
        return self.out_terminator

    @if_connected
    def get_pressure_min(self):
        return self.device.pressure_min

    @if_connected
    def set_pump_off_timer(self, off_timer):
        self.device.pump_off_timer = off_timer
        return self.out_terminator

    @if_connected
    def set_pump_on_timer(self, on_timer):
        self.device.pump_on_timer = on_timer
        return self.out_terminator

    @if_connected
    def set_valve_position(self, valve_position):
        self.device.valve_position = valve_position
        return self.out_terminator

    @if_connected
    def get_valve_position(self):
        return self.device.valve_position

    @if_connected
    def set_file_number(self, file_number):
        self.device.file_number = file_number
        return self.out_terminator

    @if_connected
    @if_input_error
    def set_file_open(self, file_number):
        self.device.file_open = True
        self.device.file_number = file_number
        return self.out_terminator

    @if_connected
    def set_file_close(self):
        self.device.file_open = False

    @if_connected
    def get_program_runtime(self):
        return self.device.program_runtime

    @if_connected
    def get_composition_a(self):
        return self.device.composition_A

    @if_connected
    def get_composition_b(self):
        return self.device.composition_B

    @if_connected
    def get_composition_c(self):
        return self.device.composition_C

    @if_connected
    def get_composition_d(self):
        return self.device.composition_D

    @if_connected
    def set_composition(self, ramptime, a, b, c):
        self.device.composition_A = a
        self.device.composition_B = b
        self.device.composition_C = c
        self.device.composition_D = 100 - (a + b + c)
        return self.out_terminator

    @if_connected
    def get_error(self):
        return self.device.error

    @if_connected
    def set_error(self):
        self.device.error = 0
        return self.out_terminator

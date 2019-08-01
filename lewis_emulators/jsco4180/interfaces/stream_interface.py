
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
            CmdBuilder(self.set_flowrate).float().escape(" flowrate set").eos().build(),
            CmdBuilder(self.get_flowrate_rbv).escape("flowrate load p").eos().build(),
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
            CmdBuilder(self.set_composition).float().escape(" ").float().escape(" ").float().escape(" ").float().escape(" comp set").eos().build(),

            CmdBuilder(self.get_error).escape("trouble load p").eos().build(),
            CmdBuilder(self.set_error).escape("0 trouble set").build(),

            CmdBuilder(self.set_pump).int().escape(" pump set").eos().build(),
            CmdBuilder(self.get_status).escape("status load p").eos().build(),

            CmdBuilder(self.set_file_number).int().escape(" fileno set").eos().build(),
            CmdBuilder(self.set_file_open).int().escape(" openfile").eos().build(),
            CmdBuilder(self.set_file_closed).int().escape(" closefile").eos().build(),
        }

    def catch_all(self):
        pass

    @if_valid_input_delay
    @if_connected
    def set_file_open(self, _):
        self.device.file_open = True

    @if_valid_input_delay
    @if_connected
    def set_file_closed(self, _):
        self.device.file_open = False

    @if_valid_input_delay
    @if_connected
    def set_file_number(self, file_number):
        state = self.device.state
        if state is not "pump_off":
            return "%%[Program is Busy]%%" + self.out_terminator
        else:
            self.device.file_number = file_number
            self.device.single_channel_mode = False

    @if_valid_input_delay
    @if_connected
    def get_status(self):
        if self.device.status == "pump_off":
            return 0
        elif self.device.status == "pump_on":
            return 33  # Running program but time halted
        elif self.device.status == "pump_program":
            return 49  # Running program with time
        elif self.device.status == "pump_program_reset":
            return 49  # Running program with reset timer

    @if_valid_input_delay
    @if_connected
    def set_pump(self, mode):
        if mode == 0:
            # Pump on
            self.device.status = "pump_on"
        elif mode == 1:
            # Pump off
            self.device.status = "pump_off"
            return self.out_terminator
        elif mode == 6:
            # Pump program (time increment halted)
            self.device.status = "pump_program"
            return self.out_terminator
        elif mode == 8:
            # Pump reset and rerun program
            self.device.status = "pump_program_reset"
            self.device.program_runtime = 0
            return self.out_terminator

    @if_valid_input_delay
    @if_connected
    @if_input_error
    def set_flowrate(self, flowrate):
        self.device.flowrate_rbv = flowrate
        return self.out_terminator

    @if_valid_input_delay
    @if_connected
    def get_flowrate(self):
        return self.device.flowrate

    @if_valid_input_delay
    @if_connected
    def get_flowrate_rbv(self):
        return self.device.flowrate_rbv

    @if_valid_input_delay
    @if_connected
    def get_current_flowrate(self):
        return self.device.flowrate

    @if_valid_input_delay
    @if_connected
    def get_pressure(self):
        return int(self.device.pressure)

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
        if self.device.status == 'pump_program_reset':
            self.device.program_runtime += 1
        return int(self.device.program_runtime)

    @if_valid_input_delay
    @if_connected
    def get_component_a(self):
        return 100 if self.device.single_channel_mode else self.device.component_A

    @if_valid_input_delay
    @if_connected
    def get_component_b(self):
        return 0 if self.device.single_channel_mode else self.device.component_B

    @if_valid_input_delay
    @if_connected
    def get_component_c(self):
        return 0 if self.device.single_channel_mode else self.device.component_C

    @if_valid_input_delay
    @if_connected
    def get_component_d(self):
        return 0 if self.device.single_channel_mode else self.device.component_D

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

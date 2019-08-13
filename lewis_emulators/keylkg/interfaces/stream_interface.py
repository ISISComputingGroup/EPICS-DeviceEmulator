from lewis.adapters.stream import StreamInterface, Cmd

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply
from enum import Enum

if_connected = conditional_reply('connected')
if_input_error = conditional_reply('input_correct', "ER,OF,00")


class Modes(Enum):
    """
    Pump Modes
    """
    MEASURE = 'R0'
    SET_UP = 'Q0'


class KeylkgStreamInterface(StreamInterface):

    terminator = '\r'

    def __init__(self):

        super(KeylkgStreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.set_mode).arg("Q0|R0").eos().build(),
            CmdBuilder(self.set_offset).escape("SW,OF,").int().escape(",").float().eos().build(),
            CmdBuilder(self.get_offset).escape("SR,OF,").float().eos().build(),
            CmdBuilder(self.get_measurement_mode).escape("SR,HB,").int().eos().build(),
            CmdBuilder(self.set_measurement_mode).escape("SW,HB,").int().escape(",").int().eos().build(),
            CmdBuilder(self.get_value_output).escape("M").int().eos().build(),
            CmdBuilder(self.reset_output).escape("VR,").int().eos().build(),
        }

    @if_connected
    def reset_output(self, output):
        if self.device.mode == "Q0":
            return "ER,VR,01"
        else:
            if output == 0:
                self.device.output1_raw_value = 0.0000
                self.device.output2_raw_value = 0.0000
            elif output == 1:
                self.device.output1_raw_value = 0.0000
            elif output == 2:
                self.device.output2_raw_value = 0.0000
            return "VR"

    @if_connected
    def get_value_output(self, output):
        m1_offset_measurement = self.device.output1_raw_value - self.device.output1_offset
        m2_offset_measurement = self.device.output2_raw_value - self.device.output2_offset

        if output == 0:
            return "ER,M0,01" if self.device.mode == Modes.SET_UP else "M0,{0:+08.4f},{1:+08.4f}".format(m1_offset_measurement,
                                                                                                         m2_offset_measurement)
        elif output == 1:
            return "ER,M1,01" if self.device.mode == Modes.SET_UP else "M1,{:+08.4f}".format(m1_offset_measurement)
        elif output == 2:
            return "ER,M2,01" if self.device.mode == Modes.SET_UP else "M2,{:+08.4f}".format(m2_offset_measurement)

    @if_connected
    def set_measurement_mode(self, head, function):
        if self.device.mode == "R0":
            return "ER,HB,01"
        else:
            if head == 1:
                self.device.head1_measurement_mode = function
            elif head == 2:
                self.device.head2_measurement_mode = function
            return "SW,HB"

    @if_connected
    def get_measurement_mode(self, head):
        if self.device.mode == "R0":
            return "ER,HB,01"
        else:
            if head == 1:
                return "SR,HB,1,{0}".format(self.device.head1_measurement_mode)
            elif head == 2:
                return "SR,HB,2,{0}".format(self.device.head2_measurement_mode)

    @if_connected
    @if_input_error
    def set_offset(self, output, offset_value):
        # The device requires a +07d formatted input that is converted to within the
        # (-99.999, 99.000) limits. We convert this so that our read back will be correct.
        converted_value = offset_value * 10e-5

        if self.device.mode == "R0":
            return "ER,OF,01"
        else:
            if output == 0:
                self.device.output1_offset = converted_value
                self.device.output2_offset = converted_value
            elif output == 1:
                self.device.output1_offset = converted_value
            elif output == 2:
                self.device.output2_offset = converted_value
            return "SW,OF"

    @if_connected
    def get_offset(self, output):
        if self.device.mode == "R0":
            return "ER,OF,01"
        else:
            if output == 1:
                return "SR,OF,1,{:+08.4f}".format(self.device.output1_offset)
            elif output == 2:
                return "SR,OF,2,{:+08.4f}".format(self.device.output2_offset)

    @if_connected
    def set_mode(self, new_mode):
        if self.device.mode == new_mode:
            print("Testing mode: {mode} {mode_binary}".format(self.device.mode, self.device.mode.MEASURE))
            print("MODE ALREADY IN TARGET MODE")
            return "ER,{mode},01".format(mode=new_mode)
        else:
            self.device.mode = Modes(new_mode)
            return new_mode

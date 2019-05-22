from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder


class Tti355StreamInterface(StreamInterface):

    in_terminator = "\n"
    out_terminator = "\r\n"
       
    def __init__(self):

        super(Tti355StreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            #CmdBuilder(self.get).escape("*IDN?").eos().build(),
            CmdBuilder(self.get_voltage_sp).escape("V?").eos().build(),
            CmdBuilder(self.set_voltage_sp).escape("V ").float().eos().build(),
            CmdBuilder(self.get_voltage).escape("VO?").eos().build(),
        }

    def catch_all(self):
        pass
    
    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    def get_voltage(self):
        volt = self.device.get_voltage()
        return "V{:.2f}".format(volt)
    
    def get_voltage_sp(self):
        return "V{:.2f}".format(self.device.voltage_sp)

    def set_voltage_sp(self, voltage_sp):
        self.device.set_voltage_sp(float(voltage_sp))
        return self.out_terminator

from lewis.adapters.stream import StreamInterface
from lewis_emulators.utils.command_builder import CmdBuilder


class Tti355StreamInterface(StreamInterface):

    in_terminator = "\n"
    out_terminator = "\r\n"
       
    def __init__(self):

        super(Tti355StreamInterface, self).__init__()

        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.get_identity).escape("*IDN?").eos().build(),
            
            CmdBuilder(self.get_voltage_sp).escape("V?").eos().build(),
            CmdBuilder(self.set_voltage_sp).escape("V ").float().eos().build(),
            CmdBuilder(self.get_voltage).escape("VO?").eos().build(),

            CmdBuilder(self.get_current_sp).escape("I?").eos().build(),
            CmdBuilder(self.set_current_sp).escape("I ").float().eos().build(),
            CmdBuilder(self.get_current).escape("IO?").eos().build(),

            CmdBuilder(self.get_outputstatus).escape("OUT?").eos().build(),
            CmdBuilder(self.set_outputstatus_on).escape("ON").eos().build(),
            CmdBuilder(self.set_outputstatus_off).escape("OFF").eos().build(),
           
            CmdBuilder(self.get_output_mode).escape("M?").eos().build(),
            CmdBuilder(self.get_error_status).escape("ERR?").eos().build(),

        }

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

    def get_current(self):
        current = self.device.get_current()
        return "I{:.2f}".format(current)
    
    def get_current_sp(self):
        return "I{:.2f}".format(self.device.current_sp)

    def set_current_sp(self, current_sp):
        self.device.set_current_sp(float(current_sp))
        return self.out_terminator

    def get_outputstatus(self):
        return self.device.get_output_status()

    def set_outputstatus_on(self):
        self.device.set_output_status("ON")
        return self.out_terminator

    def set_outputstatus_off(self):
        self.device.set_output_status("OFF")
        return self.out_terminator
    
    def get_output_mode(self):
        return self.device.get_output_mode()
    
    def get_error_status(self):
        return self.device.get_error_status()
    
    def get_identity(self):
        return self.device.identity
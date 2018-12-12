from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder

@has_log
class TtiplpStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("ident").escape("*IDN?").eos().build(),
        CmdBuilder("get_volt_sp").escape("V").int().escape("?").eos().build(),
        CmdBuilder("set_volt_sp").escape("V").int().escape(" ").float().eos().build(),
        CmdBuilder("get_volt").escape("V").int().escape("O?").eos().build(),
        CmdBuilder("get_curr_sp").escape("I").int().escape("?").eos().build(),
        CmdBuilder("set_curr_sp").escape("I").int().escape(" ").float().eos().build(),
        CmdBuilder("get_curr").escape("I").int().escape("O?").eos().build(),
        CmdBuilder("get_output").escape("OP").int().escape("?").eos().build(),
        CmdBuilder("set_output").escape("OP").int().escape(" ").float().eos().build(),
        CmdBuilder("set_overvolt").escape("OVP").int().escape(" ").float().eos().build(),
        CmdBuilder("get_overvolt").escape("OVP").int().escape("?").eos().build(),
        CmdBuilder("set_overcurr").escape("OCP").int().escape(" ").float().eos().build(),
        CmdBuilder("get_overcurr").escape("OCP").int().escape("?").eos().build(),
    }
    
    in_terminator = "\n"
    out_terminator = "\r\n"

#    def catch_all(self):
#        pass

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    def ident(self):
        return self.device.ident

    def get_volt(self,_):
        volt=self.device.get_volt()
        return "{:.4f}V".format(volt)

    def get_curr(self,_):
        curr=self.device.get_curr()
        return "{:.4f}A".format(curr)

    def set_volt_sp(self, _, volt_sp):
        self.device.set_volt_sp(float(volt_sp))

    def get_volt_sp(self,_):
        return "V1 {:.3f}".format(self.device.volt_sp)

    def set_curr_sp(self, _, curr_sp):
        self.device.set_curr_sp(float(curr_sp))

    def get_curr_sp(self,_):
        return "I1 {:.4f}".format(self.device.curr_sp)

    def set_output(self,_,output):
        self.device.set_output(output)

    def get_output(self,_):
        return "{:.0f}".format(self.device.output)

    def set_overvolt(self, _, overvolt):
        self.device.set_overvolt(float(overvolt))

    def get_overvolt(self,_):
        return "{:.3f}".format(self.device.overvolt)

    def set_overcurr(self, _, overcurr):
        self.device.set_overcurr(float(overcurr))

    def get_overcurr(self,_):
        return "{:.4f}".format(self.device.overcurr)

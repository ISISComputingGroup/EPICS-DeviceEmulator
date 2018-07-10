from lewis.adapters.stream import StreamInterface, Cmd
from lewis_emulators.utils.command_builder import CmdBuilder
from random import random as rnd

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

    def set_volt_sp(self, _, volt_sp):
        self.device.volt_sp = float(volt_sp)
        if float(volt_sp)>float(self.device.overvolt):
            self.device.output=0
            self.device.volt=0
            self.device.current=0
        #self.device.volt = float(volt_sp)

    def get_volt_sp(self,_):
        return "V1 {:.3f}".format(self.device.volt_sp)
        
    def get_volt(self,_):
        if self.device.output==1:
            self.device.volt=self.device.volt_sp+((rnd()-0.5)/1000)
        else:
            self.device.volt=((rnd()-0.5)/1000)
        return "{:.4f}V".format(self.device.volt)
        
    def set_curr_sp(self,_, curr_sp):
        self.device.curr_sp = float(curr_sp)
        if float(curr_sp)>float(self.device.overcurr):
            self.device.output=0
            self.device.volt=0
            self.device.current=0

    def get_curr_sp(self,_):
        return "I1 {:.4f}".format(self.device.curr_sp)
                
    def get_curr(self,_):
        if self.device.output==1:
            self.device.curr=self.device.curr_sp+((rnd()-0.5)/1000)
        else:
            self.device.curr=((rnd()-0.5)/1000)
        return "{:.4f}A".format(self.device.curr)
    
    def get_output(self,_):
        return "{:.0f}".format(self.device.output)
        
    def set_output(self,_,output):
        if ((self.device.volt_sp<=self.device.overvolt) and (self.device.curr_sp<=self.device.overcurr) and int(output)==1):
            self.device.output = 1
        else:
            self.device.output = 0
    
    def set_overvolt(self,_,overvolt):
        print "Here"
        self.device.overvolt = float(overvolt)
        if float(overvolt)<self.device.volt_sp:
            self.device.volt=0
            self.device.curr=0
            self.device.output=0
        
    def get_overvolt(self,_):
        return "{:.3f}".format(self.device.overvolt)

    def set_overcurr(self,_,overcurr):
        self.device.overcurr = float(overcurr)
        if float(overcurr)<self.device.curr_sp:
            self.device.volt=0
            self.device.curr=0
            self.device.output=0
        
    def get_overcurr(self,_):
        return "{:.4f}".format(self.device.overcurr)

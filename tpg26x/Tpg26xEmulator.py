import sys
from telnet_engine import TelnetEngine, ENQ_SIGNAL, ACK_SIGNAL, NAK_SIGNAL

"""Prefix for command sent to emulator to change the state of the emulator"""
EMULATOR_COMMAND_PREFIX = "emulator:"

sys.path.append("../test_framework")


class Tpg26xEmulator:
    """
    Emulator for the TPG26x pressure reading device
    """

    def __init__(self):
        """
        Constructor
        :return:
        """
        self.pressure2 = 0.08
        self.pressure1 = 0.3
        self.error2 = 1
        self.error1 = 0
        self.params = []
        self.enquire = None
        self.units = 1

    def process(self, data):
        """
        process the incoming data and return the answer
        :param data: data sent
            :type data: str
        :return: response
        """
        try:
            if data.startswith(EMULATOR_COMMAND_PREFIX):
                return self._do_emulator_command(data[len(EMULATOR_COMMAND_PREFIX):])
            elif data == chr(5):
                return self._make_enquiry()
            else:
                self.enquire = None
                self.params = None
                tokens = data.split(',')
                if len(tokens) == 0:
                    return None
                if len(tokens) > 0:
                    self.enquire = tokens[0]
                if len(tokens) > 1:
                    return self._set_value(tokens[1:])
                else:
                    return ENQ_SIGNAL

        except (ValueError, TypeError) as ex:
            print "Exception thrown during emulation: {0}".format(ex)

    def _do_emulator_command(self, command):
        """
        Perform the emulator state change based on the command
        :param command: command that was sent (without the prfix)
        :return: response
        """
        parameters = command.split()
        if parameters[0] == "set:pressure1":
            self.pressure1 = float(parameters[1])
        elif parameters[0] == "set:pressure2":
            self.pressure2 = float(parameters[1])
        elif parameters[0] == "set:error1":
            self.error1 = int(parameters[1])
        elif parameters[0] == "set:error2":
            self.error2 = int(parameters[1])
        elif parameters[0] == "set:units":
            self.units = int(parameters[1])
        return None

    def _make_enquiry(self):
        """
        Most commands sent are in two parts a command which either sets or asks for a value and then
        an enquirey that gets the response. This function deals with the response to an enquiry
        :return: response
        """
        if self.enquire == "PRX":
            #x,sx.xxxxEsxx,y,sy.yyyyEsyy
            return "{error1:1d},{pressure1:+011.4E},{error2:1d},{pressure2:011.4E}".format(
                error1=self.error1,
                pressure1=self.pressure1,
                error2=self.error2,
                pressure2=self.pressure2
            )
        elif self.enquire == "UNI":
            return "{0:1d}".format(self.units)

    def _set_value(self, values):
        """
        Set a value based on an instruction from the IOC
        :param values: value to set
        :return: response
        """
        if self.enquire == "UNI":
            self.units = int(values[0])
            return ACK_SIGNAL
        else:
            print "Error trying to set {0} which the simulator can not".format(self.enquire)
            return NAK_SIGNAL

if __name__ == "__main__":
    port_file = __file__
    dev = Tpg26xEmulator()
    TelnetEngine().start(dev, port_file)

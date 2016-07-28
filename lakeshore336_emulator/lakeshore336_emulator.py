import sys
sys.path.append("../test_framework")

from telnet_engine import TelnetEngine

class LakeshoreInput:
    def __init__(self):
        self.name = "Default Name"

class Lakeshore336Emulator:
    def __init__(self):
        self.id = "EmulatedDevice"

        self.inputs = dict()
        self.inputs["A"] = LakeshoreInput()
        self.inputs["B"] = LakeshoreInput()
        self.inputs["C"] = LakeshoreInput()
        self.inputs["D"] = LakeshoreInput()

    def process(self, data):
        if data == "*IDN?":
            return self._reply("LSCI," + self.id)

        if data.startswith("INNAME?"):
            index = data[-1]
            return self._reply(self.inputs[index].name)

        if data.startswith("INNAME"):
            tokens = data[len("INNAME "):].split(",")
            index = tokens[0]
            new_name = tokens[1].strip("\"")
            self.inputs[index].name = new_name
            return None

        return None

    def _reply(self, msg):
        return msg + "\r\n"


if __name__ == "__main__":
    port_file = __file__
    dev = Lakeshore336Emulator()
    TelnetEngine().start(dev, port_file)




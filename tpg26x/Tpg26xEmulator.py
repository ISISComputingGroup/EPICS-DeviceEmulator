import sys

sys.path.append("../test_framework")


from telnet_engine import TelnetEngine


class Tpg26xEmulator:
    def __init__(self):
        self.pressure2 = 0.08
        self.pressure1 = 0.3
        self.error2 = 1
        self.error1 = 0
        self.params = []
        self.enquire = None

    def process(self, data):
        """
        process the incoming data
        :param data: data
            :type data: str
        :return:
        """
        if data == chr(5):
            return self._make_enquirey()
        else:
            self.enquire = None
            self.params = None
            tokens = data.split(',')
            if len(tokens) > 0:
                self.enquire = tokens[0]
            if len(tokens) > 1:
                self.params = tokens[1:]

            return "\x06"


    def _make_enquirey(self):
        if self.enquire == "PRX":
            #x,sx.xxxxEsxx,y,sy.yyyyEsyy
            return "{error1:1d},{pressure1:+011.4E},{error2:1d},{pressure2:011.4E}".format(
                error1=self.error1,
                pressure1=self.pressure1,
                error2=self.error2,
                pressure2=self.pressure2
            )
        elif self.enquire == "UNI":
            return "1"

if __name__ == "__main__":
    port_file = __file__
    dev = tpg26xEmulator()
    TelnetEngine().start(dev, port_file)

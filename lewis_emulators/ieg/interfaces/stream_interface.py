from lewis.adapters.stream import StreamAdapter, Cmd
from lewis.core.logging import has_log


class IegStreamInterface(StreamAdapter):

    # Commands that we expect via serial during normal operation
    commands = {
        Cmd("get_status", "^&STS0$"),
        Cmd("change_operating_mode", "^&OPM([1-4])$"),
        Cmd("abort", "^&KILL$"),
    }

    in_terminator = "!"
    out_terminator = "\r\n"

    def _build_valve_state(self):
        val = 0
        val += 1 if self._device.pump_valve_open is True else 0
        val += 2 if self._device.buffer_valve_open is True else 0
        val += 4 if self._device.gas_valve_open is True else 0
        return val

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)

    def get_status(self):
        pass

    @has_log
    def change_operating_mode(self, mode):
        self.log.info("Setting mode to {}".format(mode))
        self._device.operatingmode = int(mode)
        return ResponseBuilder()\
            .ack()\
            .startdata()\
            .data("IEG").data(self._device.unique_id)\
            .separator()\
            .data("OPM").data(self._build_valve_state())\
            .enddata()\
            .build()

    def abort(self):
        self._device.operatingmode = 0


class ResponseBuilder(object):
    """
    Response builder for the IEG
    """

    def __init__(self):
        """
        Initialize a new response
        """
        self.response = ""

    def ack(self):
        """
        Add an ACK data packet to the response
        :return: ResponseBuilder
        """
        self.response += "&ACK!{term}".format(term=IegStreamInterface.out_terminator)
        return self

    def startdata(self):
        """
        Adds the character signifying the start of a data block
        :return: ResponseBuilder
        """
        self.response += "&"
        return self

    def separator(self):
        """
        Adds the character signifying the seperator between bits of data
        :return: ResponseBuilder
        """
        self.response += ","
        return self

    def data(self, data):
        """
        Adds data to the response being built
        :param data: the data to add
        :return: ResponseBuilder
        """
        self.response += str(data)
        return self

    def enddata(self):
        """
        Adds the 'end data' character to the response
        :return: ResponseBuilder
        """
        self.response += "!"
        return self

    def build(self):
        """
        Extract the response from the builder
        :return: (str) response
        """
        return self.response
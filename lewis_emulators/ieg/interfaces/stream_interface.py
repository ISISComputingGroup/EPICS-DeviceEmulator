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
        val += 1 if self._device.is_pump_valve_open() else 0
        val += 2 if self._device.is_buffer_valve_open() else 0
        val += 4 if self._device.is_gas_valve_open() else 0
        return val

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return str(error)

    def get_status(self):
        return ResponseBuilder() \
            .ack() \
            .startpacket() \
            .add_data_block("IEG", self._device.get_id()) \
            .add_data_block("OPM", self._device.get_operating_mode()) \
            .add_data_block("VST", self._build_valve_state()) \
            .add_data_block("ERR", self._device.get_error()) \
            .add_data_block("BPH", 0 if self._device.is_buffer_pressure_high() else 1) \
            .add_data_block("SPL", 1 if self._device.is_sample_pressure_low() else 0) \
            .add_data_block("SPH", 1 if self._device.is_sample_pressure_high() else 0) \
            .add_data_block("SPR", int(self._device.get_pressure())) \
            .endpacket() \
            .build()

    def change_operating_mode(self, mode):
        self._device.operatingmode = int(mode)
        return ResponseBuilder()\
            .ack()\
            .startpacket()\
            .add_data_block("IEG", self._device.get_id()) \
            .add_data_block("OPM", self._device.get_operating_mode())\
            .endpacket()\
            .build()

    def abort(self):
        self._device.operatingmode = 0
        return ResponseBuilder() \
            .ack() \
            .startpacket() \
            .add_data_block("IEG", self._device.get_id()) \
            .add_data_block("KILL") \
            .endpacket() \
            .build()


class ResponseBuilder(object):
    """
    Response builder for the IEG
    """
    packet_start = "&"
    packet_end = "!"
    data_block_sep = ","

    def __init__(self):
        """
        Initialize a new response
        """
        self.response = ""

    def ack(self):
        """
        Add an ACK data packet, complete with terminator, to the response
        :return: ResponseBuilder
        """
        self.response += "{pack_start}ACK{pack_end}{term}".format(pack_start=self.packet_start,
                                                                  pack_end=self.packet_end,
                                                                  term=IegStreamInterface.out_terminator)
        return self

    def startpacket(self):
        """
        Adds the character signifying the start of a data block
        :return: ResponseBuilder
        """
        self.response += self.packet_start
        return self

    def endpacket(self):
        """
        Adds the 'end data' character to the response
        :return: ResponseBuilder
        """
        self.response += self.packet_end
        return self

    def add_data_block(self, *data):
        """
        Adds a data block.
        The elements are converted to strings and added to the response in order.
        If the preceding character is not already a separator nor the start of the data block a separator is added first
        :param data: data to add to the response
        :return: ResponseBuilder
        """
        if not self.response[-1:] == self.data_block_sep and not self.response[-1:] == self.packet_start:
            self.response += self.data_block_sep

        for item in data:
            self.response += "{}".format(item)
        return self

    def build(self):
        """
        Extract the response from the builder
        :return: (str) response
        """
        return self.response

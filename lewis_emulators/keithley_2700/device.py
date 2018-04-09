from collections import OrderedDict
import random
from lewis.core.logging import has_log
from .states import DefaultState
from lewis.devices import StateMachineDevice

class Channel(object):
    def __init__(self, channel):
        self.channel = channel
        self.reading = 0
        self.timestamp = 0

@has_log
class SimulatedKeithley2700(StateMachineDevice):
    """
    Simulated Keithley2700 Multimeter
    """

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.idn = "KEITHLEY"
        self.buffer_full = []
        self.buffer_range_readings = ""
        self.measurement = "FRES"
        self.buffer_feed = "SENS"
        self.buffer_control = "NEXT"
        self.buffer_autoclear_state = 0
        self.next_buffer_location = 0
        self.bytes_used = 0
        self.bytes_available = 0
        self.buffer_size = 55000
        self.time_stamp_format = "ABS"
        self.delay_state = 1
        self.init_state = 0
        self.sample_count = 1
        self.source = "EXT"
        self.data_elements = ""
        self.auto_range_status = 1
        self.measurement_digits = 6
        self.nplc = 5.0
        self.scan_state_status = "NONE"
        self.scan_channel_start = 101
        self.scan_channel_end = 210
        self.buffer_count = 10
        self.current_buffer_loc = 0

        # Create channels from 101-110 and 201 - 210
        self.channels = []
        for i in range(1, 11):
            self.channels.append(Channel(str(100+i)))
            self.channels.append(Channel(str(200+i)))
        self.generate_channel_values()
        self.fill_buffer()

    # Populate channels with read values and timestamps
    def generate_channel_values(self):
        timestamp = 0
        for t in self.channels:
            if t.timestamp > timestamp:
                timestamp = t.timestamp

        for c in range(len(self.channels)):
            self.channels[c].reading = random.uniform(1000.0, 1500.0)
            self.channels[c].timestamp = timestamp
            timestamp += 0.005

    def fill_buffer(self):
        i = 0
        self.buffer_full = []
        self.generate_channel_values()
        self.current_buffer_loc = 0
        self.next_buffer_location = 0
        for b in range(self.buffer_size):
            if i == len(self.channels):
                self.generate_channel_values()
                i = 0
            self.channels[i].buffer_loc = b
            channel_string = "{},{},{},".format(self.channels[i].reading,
                                                self.channels[i].timestamp,
                                                self.channels[i].channel)
            self.buffer_full.append(channel_string)
            i += 1

    def set_channel_param(self, index, param, value):
        """
        Sets Attribute for Channel Instance within self.channels list
        :param index: (Integer) position in list
        :param param: Attribute
        :param value: Attribute Value
        """
        setattr(self.channels[int(index)], str(param), value)

    def get_channel_param(self, index, param):
        """
        Gets Attribute for Channel Instance within self.channels list
        :param index: (Integer) position in list
        :param param: Attribute
        :return: str
        """
        return getattr(self.channels[int(index)], str(param))

    def _get_state_handlers(self):
        """
        Returns: states and their names
        """
        return {DefaultState.NAME: DefaultState()}

    def _get_initial_state(self):
        """
        Returns: the name of the initial state
        """
        return DefaultState.NAME

    def _get_transition_handlers(self):
        """
        Returns: the state transitions
        """
        return OrderedDict()

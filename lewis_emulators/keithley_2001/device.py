from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from utils import Channel

import random


class SimulatedKeithley_2001(StateMachineDevice):
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
        self.measurement = 0
        self.buffer_feed = 0
        self.buffer_control = 0
        self.buffer_autoclear_on = False
        self.next_buffer_location = 0
        self.bytes_used = 0
        self.bytes_available = 0
        self.buffer_size = 55000
        self.time_stamp_format = 0
        self.auto_delay_on = True
        self.init_state_on = False
        self.sample_count = 1
        self.source = 4
        self.data_elements = ""
        self.auto_range_on = True
        self.measurement_digits = 6
        self.nplc = 5.0
        self.scan_state_status = 2
        self.scan_channel_start = 101
        self.scan_channel_end = 210
        self.buffer_count = 10
        self.current_buffer_loc = 0

        # Create channels from 101-110 and 201 - 210
        self.channels = []
        for i in range(1, 11):
            self.channels.append(Channel(str(0+i)))
        self.generate_channel_values()
        self.fill_buffer()

    def generate_channel_values(self):
        """
        Creates a random selection of channel resistance reading values
        :return:
        """
        timestamp = 0
        # Find current highest timestamp
        timestamp = max(t.timestamp for t in self.channels)

        for channel in self.channels:
            channel.reading = random.uniform(1000.0, 1500.0)
            channel.timestamp = timestamp
            timestamp += 0.005

    def fill_buffer(self):
        """
        Creates a new set of channel reading values and fills the buffer
        with these readings.
        The buffer values are then parsed by the IOC into the appropriate channel PVs.
        """
        chan_index = 0
        self.buffer_full = []
        self.generate_channel_values()
        self.current_buffer_loc = 0
        self.next_buffer_location = 0
        for buffer_index in range(self.buffer_size):
            # If we reach the end of the channel readings, create a new set of channel readings to fill buffer with
            if chan_index == len(self.channels):
                self.generate_channel_values()
                chan_index = 0
            channel_string = "{},{},{},".format(self.channels[chan_index].reading,
                                                self.channels[chan_index].timestamp,
                                                self.channels[chan_index].channel)
            self.buffer_full.append(channel_string)
            chan_index += 1

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
        :return: Channel parameter (int or double)
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

from collections import OrderedDict
from lewis.core.logging import has_log
from .states import DefaultState
from lewis.devices import StateMachineDevice


MAX_READ = 1500
MIN_READ = 1000


class Channel(object):
    def __init__(self):
        self.reading = 0
        self.timestamp = 0


class BufferReading(object):
    def __init__(self, reading, timestamp, channel):
        self.reading = reading
        self.timestamp = timestamp
        self.channel = channel


@has_log
class SimulatedKeithley2700(StateMachineDevice):
    """
    Simulated Keithley2700 Multimeter
    """

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.idn = "KEITHLEY"               # Device name 
        self.buffer = []                    # The buffer in which samples are stored
        self.buffer_range_readings = ""     # String containing readings from a range of channels 
        self.measurement = 0                # Measurement type. See stream_interface for options
        self.buffer_feed = 0                # source of readings (SENSe | CALCulate | NONE)
        self.buffer_control = 0             # buffer control (NEXT | ALWays | NEVer)
        self.buffer_autoclear_on = False    # when false, new readings appended to old readings in buffer
        self.next_buffer_location = 0       # index of next free buffer location
        self.bytes_used = 0                 # bytes used in buffer 
        self.bytes_available = 0            # bytes free in buffer
        self.buffer_size = 1000             # size of buffer which holds read data default 1000
        self.time_stamp_format = 0          # sets format for timestamps (ABSolute | DELta)
        self.auto_delay_on = True           # auto delay based on voltage range
        self.init_state_on = False          # initiation from idle state
        self.sample_count = 1               # number of samples taken per channel per measurement
        self.source = 4                     # ================ ?
        self.data_elements = ""             # list of data types to get (read, unit, timestamp, chnl num, limits)
        self.auto_range_on = True           # auto voltage range
        self.measurement_digits = 6         # precision of measurements taken 
        self.nplc = 5.0                     # plc rate
        self.scan_state_status = 0          # ROUTe:SCAN:LSELect 1 for INTernal (enable scan) 0 for NONE (disable)
        self.scan_channel_start = 101       # starting channel in list to be scanned
        self.scan_channel_end = 210         # end channel in list to be scanned 
        self.buffer_count = 10              # Number of samples to return. see $(P)COUNT in keithley_2700.db

        # Create channels from 101-110 and 201 - 210
        self.channels = {}
        for i in range(101, 110+1):
            self.channels[str(i)] = Channel()
        for i in range(201, 210+1):
            self.channels[str(i)] = Channel()

    def get_next_buffer_location(self):
        if not self.is_buffer_full():
            return len(self.buffer)
        else:
            return 0  # Buffer full so next loc is 0 after a clear

    def is_buffer_full(self):
        return len(self.buffer) >= self.buffer_size  # -1 because buffer is 0 indexed

    def insert_mock_data(self, data):
        """
        Allows the insertion of specific, defined readings into the buffer
        :param data: a list containing string representations of buffer readings
        """
        self.log.info("Inserting mock data into buffer: {}".format(data))
        for item in data:
            reading, timestamp, channel = item.split(",")
            if self.is_buffer_full() and self.buffer_autoclear_on:
                self.clear_buffer()
            self.buffer.append(BufferReading(reading, timestamp, channel))

    def check_buffer_data(self):
        """
        Gets values contained in self.buffer
        :return: List of comma separated string representations of readings in the buffer
        """
        return [",".join((reading.reading, reading.timestamp, reading.channel))
                .encode("utf-8") for reading in self.buffer]

    def clear_buffer(self):
        """
        Clears all buffer entries
        """
        self.buffer = []
        self.log.info("=== Cleared Buffer ===")

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

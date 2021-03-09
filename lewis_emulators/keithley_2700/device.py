from collections import OrderedDict
from lewis.core.logging import has_log
from .states import DefaultState
from lewis.devices import StateMachineDevice
from random import randint
import time
import threading

MAX_READ = 1500
MIN_READ = 1000


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

    def _simulate_readings_thread(self):
        """
        Generates random simulated data to put insert into the buffer.
        """

        def i_to_channel(i):
            """
            formats index as channel number, 101 to 110, 201 to 210
            """
            if i < 10:
                return 101 + i
            else:
                return 191 + i

        i = 0
        while self.simulate_readings:
            resistance = randint(1000, 2000)
            timestamp = time.time() - self.start_time
            self.insert_mock_data(["+{},{},+{}".format(resistance, timestamp, i_to_channel(i))])
            i = (i + 1) % 20
            time.sleep(0.1)

    @property
    def simulate_readings(self):
        return self._simulate_readings

    @simulate_readings.setter
    def simulate_readings(self, new_value):
        self.log.info(f"Setting simulate readings to {new_value}")
        self._simulate_readings = new_value

    def _initialize_data(self):
        """
        Initialize the device's attributes necessary for testing.
        """
        self.idn = "KEITHLEY"               # Device name 
        self.buffer = []                    # The buffer in which samples are stored
        self.buffer_autoclear_on = False    # when false, new readings appended to old readings in buffer
        self.buffer_size = 1000             # size of buffer which holds read data default 1000
        # The below attributes are not used but are needed for the stream interface
        self.bytes_available = 0
        self.bytes_used = 0
        self.start_time = time.time()
        self.simulate_readings = True
        thread = threading.Thread(group=None, target=self._simulate_readings_thread)
        thread.daemon = True
        thread.start()

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

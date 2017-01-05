from lewis.devices import Device
from two_gas_mixer import TwoGasMixer
from buffer import Buffer
from gas import Gas
from system_gases import SystemGases
from seed_gas_data import SeedGasData
from ethernet_device import EthernetDevice
from hmi_device import HmiDevice
from valve import Valve
from error_states import ErrorStates
from utilities import optional_int_string_format
from sensor import Sensor


class SimulatedVolumetricRig(Device):
    def __init__(self):
        # Set up all available gases
        self.system_gases = SystemGases([Gas(i, SeedGasData.names[i]) for i in range(len(SeedGasData.names))])

        # Set mixable gases
        self.mixer = TwoGasMixer()
        for name1, name2 in SeedGasData.mixable_gas_names():
            self.mixer.add_mixable(self.system_gases.gas_by_name(name1), self.system_gases.gas_by_name(name2))

        # Set buffers
        buffer_gases = [(self.system_gases.gas_by_name(name1),
                         self.system_gases.gas_by_name(name2))
                        for name1, name2 in SeedGasData.buffer_gas_names()]
        self._buffers = [Buffer(i + 1, buffer_gases[i][0], buffer_gases[i][1])
                         for i in range(len(buffer_gases))]

        # Set ethernet devices
        self._plc = EthernetDevice("192.168.0.1")
        self._hmi = HmiDevice("192.168.0.2")

        # Set up sensors
        self._temperature_sensors = [Sensor() for _ in range(9)]
        self._pressure_sensors = [Sensor() for _ in range(5)]

        # Set up special valves
        self._supply_valve = Valve()
        self._vacuum_extract_valve = Valve()
        self._cell_valve = Valve()

        # Misc system state variables
        self._halted = False
        self._status_code = 2
        self._errors = ErrorStates()

        # Target pressure: We can't set this via serial
        self._target_pressure = 12.34

        # Parent constructor
        super(SimulatedVolumetricRig, self).__init__()

    def identify(self):
        return "ISIS Volumetric Gas Handing Panel"

    def buffer_count(self):
        return len(self._buffers)

    def buffer(self, i):
        try:
            return next(b for b in self._buffers if b.index() == i)
        except StopIteration:
            return None

    def memory_location(self, location, as_string, length):
        return optional_int_string_format(location, as_string, length)

    def plc(self):
        return self._plc

    def hmi(self):
        return self._hmi

    def halted(self):
        return self._halted

    def halt(self):
        self._halted = True

    def pressure_sensors(self, reverse=False):
        return self._pressure_sensors if not reverse else list(reversed(self._pressure_sensors))

    def temperature_sensors(self, reverse=False):
        return self._temperature_sensors if not reverse else list(reversed(self._temperature_sensors))

    def target_pressure(self):
        return self._target_pressure

    def status_code(self, as_string=False, length=None):
        return optional_int_string_format(2, as_string, length)

    def errors(self):
        return self._errors

    def valve_count(self):
        return len(self.valves())

    def valves(self):
        return [self._supply_valve, self._vacuum_extract_valve, self._cell_valve] + \
               [b.valve for b in list(reversed(self._buffers))]

    def buffer_valve_is_open(self, buffer_number):
        buff = self.buffer(buffer_number)
        return buff.valve_is_open() if buff is not None else False

    def vacuum_valve_is_open(self):
        return self._vacuum_extract_valve.is_open

    def cell_valve_is_open(self):
        return self._cell_valve.is_open

    def open_buffer_valve(self, buffer_number):
        buff = self.buffer(buffer_number)
        if buff is not None:
            buff.open_valve(self.mixer)

    def open_cell_valve(self):
        self._cell_valve.open()

    def open_vacuum_valve(self):
        self._vacuum_extract_valve.open()

    def close_buffer_valve(self, buffer_number):
        buff = self.buffer(buffer_number)
        if buff is not None:
            buff.close_valve()

    def close_cell_valve(self):
        self._cell_valve.close()

    def close_vacuum_valve(self):
        self._vacuum_extract_valve.close()

    def buffers(self):
        return self._buffers

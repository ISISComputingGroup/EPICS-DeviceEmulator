from lewis.devices import Device
from two_gas_mixer import TwoGasMixer
from buffer import Buffer
from gas import Gas
from system_gases import SystemGases
from seed_gas_data import SeedGasData
from ethernet_device import EthernetDevice
from hmi_device import HmiDevice
from temperature_sensor import TemperatureSensor
from valve import Valve
from error_states import ErrorStates
from time import sleep


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
        self.buffers = [Buffer(i+1, buffer_gases[i][0], buffer_gases[i][1])
                        for i in range(len(buffer_gases))]

        # Set ethernet devices
        self._plc = EthernetDevice("192.168.0.1")
        self._hmi = HmiDevice("192.168.0.2")

        # Set up sensors
        self._temperature_sensors = [TemperatureSensor() for i in range(9)]
        self._pressure_sensors = [TemperatureSensor() for i in range(5)]

        # Set up special valves
        self.supply_valve = Valve()
        self.vacuum_extract_valve = Valve()
        self.cell_valve = Valve()

        # Misc system state variables
        self._halted = False
        self._status_code = 2
        self.errors = ErrorStates()

        # Target pressure: We can't set this via serial
        self._target_pressure = 12.34

        # Parent constructor
        super(SimulatedVolumetricRig, self).__init__()

    def identify(self):
        return "ISIS Volumetric Gas Handing Panel"

    def count_buffers(self):
        return len(self.buffers)

    def buffer(self,i):
        try:
            return next(b for b in self.buffers if b.index == i)
        except StopIteration:
            return None

    def memory_location(self, location, as_string, length):
        return self._optional_int_string_format(location, as_string, length)

    def halt(self):
        self._halted = True

    def plc_ip(self):
        return self._plc.ip

    def hmi_ip(self):
        return self._hmi.ip

    def hmi_status(self):
        return self._hmi.status

    def hmi_base_page(self, as_string=False, length=None):
        return self._optional_int_string_format(self._hmi.base_page, as_string, length)

    def hmi_sub_page(self, as_string=False, length=None):
        return self._optional_int_string_format(self._hmi.sub_page, as_string, length)

    def hmi_count_cycles(self):
        return self._hmi.count_cycles

    def halted(self):
        return self._halted

    def pressure_sensors(self, reverse=False):
        return self._pressure_sensors if not reverse else self._pressure_sensors.reverse()

    def temperature_sensors(self, reverse=False):
        return self._temperature_sensors if not reverse else self._temperature_sensors.reverse()

    def target_pressure(self):
        return self._target_pressure

    def status_code(self, as_string=False, length=None):
        return self._optional_int_string_format(2, as_string, length)

    def _optional_int_string_format(self, int, as_string, length):
        if as_string:
            return str(int) if length is not None else int[:length].zfill(length)
        else:
            return int
from two_gas_mixer import TwoGasMixer
from buffer import Buffer
from gas import Gas
from system_gases import SystemGases
from seed_gas_data import SeedGasData
from ethernet_device import EthernetDevice
from hmi_device import HmiDevice
from valve import Valve
from error_states import ErrorStates
from utilities import format_int, format_float
from sensor import Sensor
from pressure_sensor import PressureSensor
from states import DefaultInitState, DefaultRunningState
from collections import OrderedDict

from lewis.devices import StateMachineDevice


class SimulatedVolumetricRig(StateMachineDevice):

    HALTED_MESSAGE = "Rejected only allowed when running"

    def _initialize_data(self):
        self.serial_command_mode = True

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

        # Target pressure: We can't set this via serial
        self._target_pressure = 100.00

        # Set up sensors
        self._temperature_sensors = [Sensor() for _ in range(9)]
        self._pressure_sensors = [PressureSensor(self._target_pressure) for _ in range(5)]

        # Set up special valves
        self._supply_valve = Valve()
        self._vacuum_extract_valve = Valve()
        self._cell_valve = Valve()

        # Misc system state variables
        self._halted = False
        self._status_code = 2
        self._errors = ErrorStates()

    def _get_state_handlers(self):
        return {
            'init': DefaultInitState(),
            'running': DefaultRunningState(),
        }

    def _get_initial_state(self):
        return 'init'

    def _get_transition_handlers(self):
        return OrderedDict([
            (('init', 'running'), lambda: self.serial_command_mode),
        ])

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
        return format_int(location, as_string, length)

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

    def target_pressure(self, as_string):
        return format_float(self._target_pressure, as_string)

    def status_code(self, as_string=False, length=None):
        return format_int(2, as_string, length)

    def errors(self):
        return self._errors

    def valve_count(self):
        return len(self.valves_status())

    def valves_status(self):
        return [self._supply_valve.status(),
                self._vacuum_extract_valve.status(),
                self._cell_valve.status()] + \
               [b.valve_status() for b in list(reversed(self._buffers))]

    def buffer_valve_is_open(self, buffer_number):
        buff = self.buffer(buffer_number)
        return buff.valve_is_open() if buff is not None else False

    def vacuum_valve_is_open(self):
        return self._vacuum_extract_valve.is_open()

    def cell_valve_is_open(self):
        return self._cell_valve.is_open()

    def buffer_valve_is_enabled(self, buffer_number):
        buff = self.buffer(buffer_number)
        return buff.valve_is_enabled() if buff is not None else False

    def vacuum_valve_is_enabled(self):
        return self._vacuum_extract_valve.is_enabled()

    def cell_valve_is_enabled(self):
        return self._cell_valve.is_enabled()

    def open_buffer_valve(self, buffer_number):
        if not self._halted:
            buff = self.buffer(buffer_number)
            if buff is not None:
                buff.open_valve(self.mixer)

    def open_cell_valve(self):
        if not self._halted:
            self._cell_valve.open()

    def open_vacuum_valve(self):
        if not self._halted:
            if not any([b.valve_is_open() for b in self._buffers]):
                self._vacuum_extract_valve.open()

    def close_buffer_valve(self, buffer_number):
        if not self._halted:
            buff = self.buffer(buffer_number)
            if buff is not None:
                buff.close_valve()

    def close_cell_valve(self):
        if not self._halted:
            self._cell_valve.close()

    def close_vacuum_valve(self):
        if not self._halted:
            self._vacuum_extract_valve.close()

    def buffers(self):
        return self._buffers

    def update_buffer_pressures(self, dt):
        for b in self._buffers:
            b.update_pressure(dt, self._target_pressure)
        for p in self._pressure_sensors:
            p.set_value(self._buffers[0].pressure())

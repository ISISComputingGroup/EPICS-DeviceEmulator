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


class SimulatedVolumetricRig(Device):
    def __init__(self):

        names = SeedGasData.names()
        self.system_gases = SystemGases([Gas(i, names[i]) for i in range(len(names))])

        self.mixer = TwoGasMixer()
        for pair in SeedGasData.mixable_gas_names():
            self.mixer.add_mixable(self.system_gases.gas_by_name(pair.pop()), self.system_gases.gas_by_name(pair.pop()))

        # Set buffers
        buffer_gases = [(self.system_gases.gas_by_name(pair[0]),
                         self.system_gases.gas_by_name(pair[1]))
                        for pair in SeedGasData.buffer_gas_names()]
        self.buffers = [Buffer(i+1, buffer_gases[i][0], buffer_gases[i][1])
                        for i in range(len(buffer_gases))]

        # Set ethernet devices
        self.plc = EthernetDevice()
        self.hmi = HmiDevice()

        # Set up sensors
        self.temperature_sensors = [TemperatureSensor() for i in range(9)]
        self.pressure_sensors = [TemperatureSensor() for i in range(5)]

        # Target pressure: We can't set this via serial
        self.target_pressure = 12.34

        # Set up special valves
        self.supply_valve = Valve()
        self.vacuum_extract_valve = Valve()
        self.cell_valve = Valve()

        self.halted = False
        self.status_code = 2
        self.errors = ErrorStates()

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

    def memory_location(self, location):
        return str(location).zfill(6)

    def halt(self):
        self.halted = True
import time
from collections import OrderedDict
from states import PumpOff, PumpOn, PumpProgram, PumpProgramTimed
from lewis.devices import StateMachineDevice


states = OrderedDict([
    ("pump_off", PumpOff()),
    ("pump_on", PumpOn()),
    ("pump_program", PumpProgram()),
    ("pump_program_timed", PumpProgramTimed())])


class SimulatedJsco4180(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.connected = True
        self.input_correct = True
        self.single_channel_mode = False
        self.status = "pump_off"

        self.flowrate_sp = 0.1
        self.flowrate_rbv = 0.1
        self.flowrate = 0.0

        self.pressure = 0
        self.pressure_max = 400
        self.pressure_min = 1

        # Composition components A, B, C, D
        self.component_A = 100.0
        self.component_B = 0.0
        self.component_C = 0.0
        self.component_D = 0.0

        self.program_runtime = 0
        self.file_number = 0
        self.file_open = False
        self.error = 0

    @property
    def state(self):
        return self._csm.state

    def crash_pump(self):
        print("##### CRASH PUMP #####")
        self.connected = False
        print("New connected status: {}".format(self.connected))

    def attempt_single_channel_mode_reset(self):
        if self.device.file_number is not None and self.device.file_open is False:
            print("ATTEMPTING RESET")
            self.device.single_channel_mode = False

    def simulate_pumping(self):
        self.flowrate = self.flowrate_rbv
        self.pressure = (self.pressure_max - self.pressure_min) // 2

    def _get_state_handlers(self):
        return states

    def _get_initial_state(self):
        return "pump_off"

    def _get_transition_handlers(self):
        return OrderedDict([
            (("pump_on", "pump_off"), lambda: self.status == "pump_off"),
            (("pump_program", "pump_off"), lambda: self.status == "pump_off"),
            (("pump_program_timed", "pump_off"), lambda: self.status == "pump_off"),

            (("pump_off", "pump_on"), lambda: self.status == "on"),
            (("pump_off", "pump_program"), lambda: self.status == "pump_program"),
            (("pump_off", "pump_program_timed"), lambda: self.status == "pump_program_timed"),

            (("pump_on", "pump_program"), lambda: self.status == "pump_program"),
            (("pump_on", "pump_program_timed"), lambda: self.status == "pump_program_timed"),

            (("pump_program", "pump_on"), lambda: self.status == "pump_on"),
            (("pump_program", "pump_program_timed"), lambda: self.status == "pump_program_timed"),

            (("pump_program_timed", "pump_on"), lambda: self.status == "pump_on"),
            (("pump_program_timed", "pump_program"), lambda: self.status == "pump_program"),
        ])

    def reset(self):
        self._initialize_data()

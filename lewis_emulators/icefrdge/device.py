from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice


class VTILoopChannel(object):
    """
    Class to represent an individual channel for controlling loops in the VTI of an ICE dilution fridge. A channel has
    a temperature setpoint, PID values and a ramp rate.
    """

    def __init__(self):
        self.vti_loop_temp_setpoint = 0
        self.vti_loop_proportional = 0
        self.vti_loop_integral = 0
        self.vti_loop_derivative = 0
        self.vti_loop_ramp_rate = 0


class SimulatedIceFridge(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.vti_temps = [0, 0, 0, 0]

        self.vti_loop_channels = {
            1: VTILoopChannel(),
            2: VTILoopChannel()
        }

        self.lakeshore_mc_cernox = 0
        self.lakeshore_mc_ruo = 0
        self.lakeshore_still_temp = 0

        self.lakeshore_mc_temp_setpoint = 0
        self.lakeshore_scan = 0
        self.lakeshore_cmode = 0

        self.lakeshore_mc_proportional = 0
        self.lakeshore_mc_integral = 0
        self.lakeshore_mc_derivative = 0

        self.lakeshore_mc_heater_range = 0
        self.lakeshore_mc_heater_percentage = 0
        self.lakeshore_still_output = 0

        self.lakeshore_exc_voltage_range_ch5 = 1
        self.lakeshore_exc_voltage_range_ch6 = 1

        self.pressures = [0, 0, 0, 0]
        # The mimic panel has 10 valves, easier to use list comprehension than write them directly
        self.valves = [0 for i in range(10)]

        self.proportional_valves = [0, 0, 0]
        self.needle_valve = 0
        self.solenoid_valves = [0, 0]
        self.temp_1K_stage = 0

        self.mixing_chamber_temp = 0
        self.mixing_chamber_resistance = 0

        self.connected = True

        self.skipped = False
        self.stopped = False

        self.condense = False
        self.circulate = False
        self.temp_control = 0
        self.make_safe = False
        self.warm_up = False

        self.mimic_info = ""
        self.state = ""
        self.needle_valve_mode = False
        self.pump_1K = 0
        self.he3_pump = 0
        self.roots_pump = 0

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    def reset(self):
        """
        Public method that re-initializes the device's fields.
        :return: Nothing.
        """
        self._initialize_data()

    def set_cryo_temp(self, cryo_temp_num, temp_value):
        """
        Sets a vti cryo temperature to a new value.
        :param cryo_temp_num: the index of the cryo temperature, from 1 to 4.
        :param temp_value: The new temperature value.
        :return: None.
        """
        self.vti_temps[cryo_temp_num - 1] = temp_value

    def set_pressure(self, index, new_value):
        """
        Sets a mimic pressure in the mimic pressures list to a new value.
        :param index: the index of the pressure we want to set, from 1 to 4.
        :param new_value: The new pressure value.
        :return: None.
        """
        self.pressures[index - 1] = new_value

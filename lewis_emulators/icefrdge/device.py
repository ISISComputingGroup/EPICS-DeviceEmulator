from collections import OrderedDict
from states import DefaultState
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
        self.vti_temp1 = 0
        self.vti_temp2 = 0
        self.vti_temp3 = 0
        self.vti_temp4 = 0

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

        self.mimic_pressures = [0, 0, 0, 0]
        # The mimic panel has 10 valves, easier to use list comprehension than write them directly
        self.mimic_valves = [False for i in range(10)]

        self.mimic_proportional_valves = [0, 0, 0]
        self.mimic_needle_valve = 0
        self.mimic_solenoid_valves = [False, False]
        self.mimic_1K_stage = 0

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

    def set_mimic_pressure(self, index, new_value):
        """
        Sets a mimic pressure in the mimic pressures list to a new value.
        :param index: the index of the pressure we want to set, from 1 to 4.
        :param new_value: The new pressure value.
        :return: None.
        """
        self.mimic_pressures[index - 1] = new_value

    def set_mimic_valve(self, valve_number, valve_status):
        """
        Sets the status of a mimic valve in the mimic valve status list to a new value.
        :param valve_number: the index of the valve you want to set, from 1 to 10.
        :param valve_status: 1 if the valve is open, 0 if it is closed.
        :return: None
        """

        if valve_status != 0 and valve_status != 1:
            raise ValueError("the status of the valve can only be 0 or 1!")

        self.mimic_valves[valve_number - 1] = SimulatedIceFridge._int_to_bool(valve_status)

    def set_solenoid_valve(self, valve_number, valve_status):
        """
        Sets the status of a mimic solenoid valve in the mimic solenoid valve status list to a new value.
        :param valve_number: the index of the valve you want to set, from 1 to 10.
        :param valve_status: 1 if the valve is open, 0 if it is closed.
        :return: None
        """

        if valve_status != 0 and valve_status != 1:
            raise ValueError("the status of the valve can only be 0 or 1!")

        self.mimic_solenoid_valves[valve_number - 1] = SimulatedIceFridge._int_to_bool(valve_status)

    def set_mimic_proportional_valve(self, valve_number, valve_value):
        """
        Sets the status of a mimic valve in the mimic valve status list to a new value.
        :param valve_number: the index of the valve you want to set, which is 1, 2 or 4. This is because in the LabView
        software used on SECI, the mimic panel only has proportional valves 1, 2 and 4.
        :param valve_value: the new value of the valve.
        :return: None
        """

        if valve_number != 1 and valve_number != 2 and valve_number != 4:
            raise ValueError("valve number argument can only be 1, 2 or 4!")

        if valve_number == 4:
            valve_number = 3

        self.mimic_proportional_valves[valve_number - 1] = valve_value

    @staticmethod
    def _int_to_bool(integer):
        if integer == 0:
            return False
        else:
            return True

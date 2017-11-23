from collections import OrderedDict

from lewis.devices import StateMachineDevice
from .states import DefaultState


class SimulatedFZJDDFCH(StateMachineDevice):
    """
    Simulated FZJ Digital Drive Fermi Chopper Controller.
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self.frequency_reference = 0
        self.frequency_setpoint = 0
        self.frequency = 0
        self.phase_setpoint = 0
        self.phase = 0
        self.phase_status = "OK"
        self.magnetic_bearing = "OFF"
        self.magnetic_bearing_status = "OK"
        self.magnetic_bearing_integrator = 0
        self.drive = "OFF"
        self.drive_status = "START"
        self.drive_l1_current = 0
        self.drive_l2_current = 0
        self.drive_l3_current = 0
        self.is_drive_direction_clockwise = True
        self.parked_open_status = "OK"
        self.drive_temperature = 0
        self.input_clock = 0
        self.phase_outage = 0
        self.master_chopper = "C01"
        self.logging = "ON"
        self.lmsr_status = "OK"
        self.dsp_status = "OK"
        self.interlock_er_status = "OK"
        self.interlock_vacuum_status = "OK"
        self.interlock_frequency_monitoring_status = "OK"
        self.interlock_magnetic_bearing_amplifier_temperature_status = "OK"
        self.interlock_magnetic_bearing_amplifier_current_status = "OK"
        self.interlock_drive_amplifier_temperature_status = "OK"
        self.interlock_drive_amplifier_current_status = "OK"
        self.interlock_ups_status = "OK"

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

    def reset(self):
        """
        Reset device to defaults
        :return: 
        """

        self._initialize_data()

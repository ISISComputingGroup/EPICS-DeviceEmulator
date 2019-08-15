from collections import OrderedDict
from lewis.devices import StateMachineDevice
from lewis.core.statemachine import State

from lewis_emulators.Lksh218.states import DefaultState


class PumpStates(object):
    """
    The pump states
    """

    stopped = object()
    starting_delay = object()
    accelerating = object()
    running = object()
    stopping_short_delay = object()
    stopping_normal_delay = object()
    fault_braking = object()
    braking = object()


class PriorityStates(object):
    """
    Priority values
    """

    OK = object()
    warning = object()
    alarm = object()


class AlertStates(object):
    """
    Alert states
    """

    no_alert = object()
    adc_fault = object()
    adc_not_ready = object()
    over_range = object()
    under_range = object()
    adc_invalid = object()
    no_gauge = object()
    unknown = object()
    not_supported = object()
    new_id = object()
    ion_em_timeout = object()
    not_struck = object()
    filament_fail = object()
    mag_fail = object()
    striker_fail = object()
    cal_error = object()
    initialising = object()
    emission_error = object()
    over_pressure = object()
    asg_cant_zero = object()
    rampup_timeout = object()
    droop_timeout = object()
    run_hours_high = object()
    sc_interlock = object()
    id_volts_error = object()
    serial_id_fail = object()
    upload_active = object()
    dx_fault = object()
    temp_alert = object()
    sysi_inhibit = object()
    ext_inhibit = object()
    temp_inhibit = object()
    no_reading = object()
    no_message = object()
    nov_failure = object()
    upload_timeout = object()
    download_failed = object()
    no_tube = object()
    use_gauges_4to6 = object()
    degas_inhibited = object()
    igc_inhibited = object()
    brownout_short = object()
    service_due = object()


class SimulatedEdwards(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        self.turbo_pump = PumpStates.stopped
        self.turbo_priority = PriorityStates.OK
        self.turbo_alert = AlertStates.no_alert

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    @property
    def turbo_pump(self):
        """
        Gets the running state of the turbo pump
        """

        return self.turbo_pump

    @turbo_pump.setter
    def turbo_pump(self, state):
        """
        Sets the running state of the turbo pump

        Args:
            value: object, an attribute of the PumpStates class
        """

        self.turbo_pump = state

    @property
    def turbo_priority(self):
        """
        Gets the priority state of the turbo pump
        """

        return self.turbo_priority

# This setter doesn't exist on the 'real' device
    @turbo_priority.setter
    def turbo_priority(self, state):
        """
        Sets the priority state of the turbo pump

        Args:
            value: object, an attribute of the PumpStates class
        """

        self.turbo_priority = state

    @property
    def turbo_alarm(self):
        """
        Gets the alarm state of the turbo pump
        """

        return self.turbo_alarm

# This setter doesn't exist on the 'real' device
    @turbo_alarm.setter
    def turbo_alarm(self, state):
        """
        Sets the alarm state of the turbo pump

        Args:
            value: object, an attribute of the PriorityStates class
        """

        self.turbo_alarm = state


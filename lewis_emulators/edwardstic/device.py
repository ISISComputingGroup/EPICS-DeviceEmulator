from collections import OrderedDict
from lewis.devices import StateMachineDevice
from enum import Enum

from states import DefaultState


class OnOffStates(Enum):
    """
    Holds whether a device function is on or off
    """

    on = 4
    off = 0


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
    Warning = object()
    Alarm = object()

class AlertStates(Enum):
    """
    Alert states
    """
    no_alert = 0
    adc_fault = 1
    adc_not_ready = 2
    over_range = 3
    under_range = 4
    adc_invalid = 5
    no_gauge = 6
    unknown = 7
    not_supported = 8
    new_id = 9
    ion_em_timeout = 13
    not_struck = 14
    filament_fail = 15
    mag_fail = 16
    striker_fail = 17
    cal_error = 20
    initialising = 21
    emission_error = 22
    over_pressure = 23
    asg_cant_zero = 24
    rampup_timeout = 25
    droop_timeout = 26
    run_hours_high = 27
    sc_interlock = 28
    id_volts_error = 29
    serial_id_fail = 30
    upload_active = 31
    dx_fault = 32
    temp_alert = 33
    sysi_inhibit = 34
    ext_inhibit = 35
    temp_inhibit = 36
    no_reading = 37
    no_message = 38
    nov_failure = 39
    upload_timeout = 40
    download_failed = 41
    no_tube = 42
    use_gauges_4to6 = 43
    degas_inhibited = 44
    igc_inhibited = 45
    brownout_short = 46
    service_due = 47

    #no_alert = object()
    #adc_fault = object()
    #adc_not_ready = object()
    #over_range = object()
    #under_range = object()
    #adc_invalid = object()
    #no_gauge = object()
    #unknown = object()
    #not_supported = object()
    #new_id = object()
    #ion_em_timeout = object()
    #not_struck = object()
    #filament_fail = object()
    #mag_fail = object()
    #striker_fail = object()
    #cal_error = object()
    #initialising = object()
    #emission_error = object()
    #over_pressure = object()
    #asg_cant_zero = object()
    #rampup_timeout = object()
    #droop_timeout = object()
    #run_hours_high = object()
    #sc_interlock = object()
    #id_volts_error = object()
    #serial_id_fail = object()
    #upload_active = object()
    #dx_fault = object()
    #temp_alert = object()
    #sysi_inhibit = object()
    #ext_inhibit = object()
    #temp_inhibit = object()
    #no_reading = object()
    #no_message = object()
    #nov_failure = object()
    #upload_timeout = object()
    #download_failed = object()
    #no_tube = object()
    #use_gauges_4to6 = object()
    #degas_inhibited = object()
    #igc_inhibited = object()
    #brownout_short = object()
    #service_due = object()


class SimulatedEdwardsTIC(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        self._turbo_pump = PumpStates.stopped
        self._turbo_priority = PriorityStates.OK
        self._turbo_alert = 0
        self._turbo_in_standby = False
        self.is_connected = True

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
    def turbo_in_standby(self):
        """
        Gets whether the turbo is in standby mode
        
        Returns:
            _turbo_standby: Bool, True if the turbo is in standby mode
        """

        return self._turbo_in_standby

    @turbo_in_standby.setter
    def turbo_standby(self, value):
        """
        Sets the turbo standby mode

        Args:
            value: Bool, True to set standby mode. False to unset standby mode
        """

        self._turbo_in_standby = value

    def turbo_set_standby(self, value):
        """
        Sets / unsets turbo standby mode

        Args:
            value, int: 1 to set standby mode, 0 to unset standby.
        """

        if value == 1:
            self.log.info("Entering turbo standby mode")
            self._turbo_in_standby = True
        elif value == 0:
            self.log.info("Leaving turbo standby mode")
            self._turbo_in_standby = False
        else:
            raise ValueError("Invalid standby argument provided ({} not 0 or 1)".format(value))

    @property
    def turbo_pump(self):
        """
        Gets the running state of the turbo pump
        """

        return self._turbo_pump

    def turbo_start_stop(self, value):
        """
        Sets the turbo pump running/stopping

        Args:
            value: int, 1 if starting the pump 0 to stop the pump
        """

        self.log.info("Starting or stopping turbo {}".format(value))

        if value == 1:
            self.log.info("Starting turbo")
            self._turbo_pump = PumpStates.running
        elif value == 0:
            self.log.info("Stopping turbo")
            self._turbo_pump = PumpStates.stopped
        else:
            raise ValueError("Invalid start/stop switch ({} not 0 or 1)".format(value))

    @property
    def turbo_priority(self):
        """
        Gets the priority state of the turbo pump
        """

        self.log.info("Getting priority {}".format(self._turbo_priority))

        return self._turbo_priority

# This setter doesn't exist on the 'real' device
    def set_turbo_priority(self, state):
        """
        Sets the priority state of the turbo pump

        Args:
            value: object, an attribute of the PumpStates class
        """

        self.log.info("attempting to set state {}".format(state))

        priority_state = getattr(PriorityStates, state)

        self._turbo_priority = priority_state

    @property
    def turbo_alarm(self):
        """
        Gets the alarm state of the turbo pump
        """

        return self._turbo_alarm

# This setter doesn't exist on the 'real' device
    @turbo_alarm.setter
    def turbo_alarm(self, state):
        """
        Sets the alarm state of the turbo pump

        Args:
            value: object, an attribute of the PriorityStates class
        """

        self._turbo_alarm = state

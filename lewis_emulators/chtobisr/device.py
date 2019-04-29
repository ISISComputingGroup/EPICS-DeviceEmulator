from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from lewis.core.logging import has_log

class SimulatedChtobisr(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        self.id = "Coherent OBIS Laser Remote - EMULATOR"

        self.interlock = "OFF"

        self.connected = True

        self.status = 0x00000000
        self.status.laser_fault = False
        self.status.laser_emission = False
        self.status.laser_ready = False
        self.status.laser_standby = False
        self.status.cdrh_delay = False
        self.status.laser_hardware_fault = False
        self.status.laser_error = False
        self.status.laser_power_calibration = False
        self.status.laser_warm_up = False
        self.status.laser_noise = False
        self.status.external_operating_mode = False
        self.status.field_calibration = False
        self.status.laser_power_voltage = False

        self.status.controller_standby = False
        self.status.controller_interlock = False
        self.status.controller_enumeration = False
        self.status.controller_error = False
        self.status.controller_fault = False
        self.status.remote_active = False
        self.status.controller_indicator = False

        self.faults = {
            "base_plate_temp_fault": False,
            "diode_temp_fault": False,
            "internal_temp_fault": False,
            "laser_power_supply_fault": False,
            "i2c_error": False,
            "over_current": False,
            "laser_checksum_error": False,
            "checksum_recovery": False,
            "buffer_overflow": False,
            "warm_up_limit_fault": False,
            "tec_driver_error": False,
            "ccb_error": False,
            "diode_temp_limit_error": False,
            "laser_ready_fault": False,
            "photodiode_fault": False,
            "fatal_fault": False,
            "startup_fault": False,
            "watchdog_timer_reset": False,
            "field_calibration": False,
            
            "over_power": False,
            
            "controller_checksum": False,
            "controller_status": False,
        }

    def reset(self):
        """
            Resets all parameters by calling initialize function
        """

        self._initialize_data()

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    @has_log
    def backdoor_set_fault(self, faultname, value):
        """
            Sets fault code via backdoor
        :param faultname: name of attribute
        :param value: true or false
        :return: none
        """
        try:
            self.faults[faultname] = value
        except KeyError:
            self.log.error("An error occurred: " + str(KeyError))

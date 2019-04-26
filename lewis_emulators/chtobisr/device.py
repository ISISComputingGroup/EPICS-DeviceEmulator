from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedChtobisr(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        self.id = "Coherent OBIS Laser Remote - EMULATOR"

        self.interlock = "OFF"

        self.connected = True

        self.status = 00000000
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

        self.status.controller_standby = False
        self.status.controller_interlock = False
        self.status.controller_enumeration = False
        self.status.controller_error = False
        self.status.controller_fault = False
        self.status.remote_active = False
        self.status.controller_indicator = False

        self.fault = 00000000
        self.fault.base_plate_temp_fault = False
        self.fault.diode_temp_fault = False
        self.fault.internal_temp_fault = False
        self.fault.laser_power_supply_fault = False
        self.fault.i2c_error = False
        self.fault.over_current = False
        self.fault.laser_checksum_error = False
        self.fault.checksum_recovery = False
        self.fault.buffer_overflow = False
        self.fault.warm_up_limit_fault = False
        self.fault.tec_driver_error = False
        self.fault.ccb_error = False
        self.fault.diode_temp_limit_error = False
        self.fault.laser_ready_fault = False
        self.fault.photodiode_fault = False
        self.fault.fatal_fault = False
        self.fault.startup_fault = False
        self.fault.watchdog_timer_reset = False
        self.fault.field_calibration = False

        self.fault.over_power = False

        self.fault.controller_checksum = False
        self.fault.controller_status = False


    def reset(self):
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

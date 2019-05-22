from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from lewis.core.logging import has_log


class SimulatedChtobisr(StateMachineDevice):
    """
        Class to simulate Coherent OBIS Laser Remote
    """

    def _initialize_data(self):
        """
            Initialize all of the device's attributes.
        """

        self.connected = True
        self.id = "Coherent OBIS Laser Remote - EMULATOR"
        self.interlock = "OFF"  # "OFF" -> OPEN, "ON" -> CLOSED

        # Dictionary of form:
        # {status_name: [whether_in_status, return_code]}
        self.status = {
            # Laser specific status bits
            "laser_fault":              [False, 0x00000001],
            "laser_emission":           [False, 0x00000002],
            "laser_ready":              [False, 0x00000004],
            "laser_standby":            [False, 0x00000008],
            "cdrh_delay":               [False, 0x00000010],
            "laser_hardware_fault":     [False, 0x00000020],
            "laser_error":              [False, 0x00000040],
            "laser_power_calibration":  [False, 0x00000080],
            "laser_warm_up":            [False, 0x00000100],
            "laser_noise":              [False, 0x00000200],
            "external_operating_mode":  [False, 0x00000400],
            "field_calibration":        [False, 0x00000800],
            "laser_power_voltage":      [False, 0x00001000],
            # Controller specific status bits
            "controller_standby":       [False, 0x02000000],
            "controller_interlock":     [False, 0x04000000],
            "controller_enumeration":   [False, 0x08000000],
            "controller_error":         [False, 0x10000000],
            "controller_fault":         [False, 0x20000000],
            "remote_active":            [False, 0x40000000],
            "controller_indicator":     [False, 0x80000000],
        }
        
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
            # ...
            "over_power": False,
            # ...
            "controller_checksum": False,
            "controller_status": False,
        }

    @has_log
    def backdoor_set_interlock(self, value):
        """
            Sets interlock via backdoor
        :param value: "ON" or "OFF"
        :return: none
        """
        if value not in ["ON", "OFF"]:
            self.log.error("Interlock can only be set to ON or OFF")
        else:
            self.interlock = value

    def reset(self):
        """
            Resets all parameters by calling initialize function
        """

        self._initialize_data()

    def build_status_code(self):
        """"
            Builds the device status code

        :return: status code
        """
        status_code = 0x00000000

        for value in self.status.values():
            if value[0]:
                status_code += value[1]

        return status_code

    def build_fault_code(self):
        """"
            Builds the device fault code

        :return: fault code
        """
        fault_code = 0x00000000

        # Laser specific fault bits
        if self.faults["base_plate_temp_fault"]:
            fault_code += 0x00000001
        if self.faults["diode_temp_fault"]:
            fault_code += 0x00000002
        if self.faults["internal_temp_fault"]:
            fault_code += 0x00000004
        if self.faults["laser_power_supply_fault"]:
            fault_code += 0x00000008
        if self.faults["i2c_error"]:
            fault_code += 0x00000010
        if self.faults["over_current"]:
            fault_code += 0x00000020
        if self.faults["laser_checksum_error"]:
            fault_code += 0x00000040
        if self.faults["checksum_recovery"]:
            fault_code += 0x00000080
        if self.faults["buffer_overflow"]:
            fault_code += 0x00000100
        if self.faults["warm_up_limit_fault"]:
            fault_code += 0x00000200
        if self.faults["tec_driver_error"]:
            fault_code += 0x00000400
        if self.faults["ccb_error"]:
            fault_code += 0x00000800
        if self.faults["diode_temp_limit_error"]:
            fault_code += 0x00001000
        if self.faults["laser_ready_fault"]:
            fault_code += 0x00002000
        if self.faults["photodiode_fault"]:
            fault_code += 0x00004000
        if self.faults["fatal_fault"]:
            fault_code += 0x00008000
        if self.faults["startup_fault"]:
            fault_code += 0x00010000
        if self.faults["watchdog_timer_reset"]:
            fault_code += 0x00020000
        if self.faults["field_calibration"]:
            fault_code += 0x00040000
        # ...
        if self.faults["over_power"]:
            fault_code += 0x00100000

        # Controller specific fault bits
        if self.faults["controller_checksum"]:
            fault_code += 0x40000000
        if self.faults["controller_status"]:
            fault_code += 0x80000000

        return fault_code

    @has_log
    def backdoor_set_status(self, statusname, value):
        """
            Sets status code via backdoor
        :param statusname: name of status attribute
        :param value: true or false
        :return: none
        """
        try:
            self.status[statusname][0] = value
        except KeyError:
            self.log.error("An error occurred: " + KeyError.message)

    @has_log
    def backdoor_set_fault(self, faultname, value):
        """
            Sets fault code via backdoor
        :param faultname: name of fault attribute
        :param value: true or false
        :return: none
        """
        try:
            self.faults[faultname] = value
        except KeyError:
            self.log.error("An error occurred: " + KeyError.message)

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

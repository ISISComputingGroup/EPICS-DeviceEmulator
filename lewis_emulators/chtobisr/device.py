from collections import OrderedDict
from dataclasses import dataclass, field

from lewis.core.logging import has_log
from lewis.core.statemachine import State
from lewis.devices import StateMachineDevice

from .states import DefaultState


def build_code(codes_dict: dict[str, tuple[bool, int]]) -> int:
    """Builds a code based on a codes dictionary
    :param codes_dict: A dictionary with the code and whether it's flagged or not.
    :return: The full code
    """
    code = 0x00000000

    for value in codes_dict.values():
        if value[0]:
            code += value[1]

    return code


@dataclass
class ChtobisrLaser:
    id = "Coherent OBIS Laser Remote - EMULATOR"
    interlock = "OFF"

    status: dict = field(
        default_factory=lambda: {
            # Laser specific status bits
            "laser_fault": [False, 0x00000001],
            "laser_emission": [False, 0x00000002],
            "laser_ready": [False, 0x00000004],
            "laser_standby": [False, 0x00000008],
            "cdrh_delay": [False, 0x00000010],
            "laser_hardware_fault": [False, 0x00000020],
            "laser_error": [False, 0x00000040],
            "laser_power_calibration": [False, 0x00000080],
            "laser_warm_up": [False, 0x00000100],
            "laser_noise": [False, 0x00000200],
            "external_operating_mode": [False, 0x00000400],
            "field_calibration": [False, 0x00000800],
            "laser_power_voltage": [False, 0x00001000],
            # Controller specific status bits
            "controller_standby": [False, 0x02000000],
            "controller_interlock": [False, 0x04000000],
            "controller_enumeration": [False, 0x08000000],
            "controller_error": [False, 0x10000000],
            "controller_fault": [False, 0x20000000],
            "remote_active": [False, 0x40000000],
            "controller_indicator": [False, 0x80000000],
        }
    )

    faults: dict = field(
        default_factory=lambda: {
            # Laser specific fault bits
            "base_plate_temp_fault": [False, 0x00000001],
            "diode_temp_fault": [False, 0x00000002],
            "internal_temp_fault": [False, 0x00000004],
            "laser_power_supply_fault": [False, 0x00000008],
            "i2c_error": [False, 0x00000010],
            "over_current": [False, 0x00000020],
            "laser_checksum_error": [False, 0x00000040],
            "checksum_recovery": [False, 0x00000080],
            "buffer_overflow": [False, 0x00000100],
            "warm_up_limit_fault": [False, 0x00000200],
            "tec_driver_error": [False, 0x00000400],
            "ccb_error": [False, 0x00000800],
            "diode_temp_limit_error": [False, 0x00001000],
            "laser_ready_fault": [False, 0x00002000],
            "photodiode_fault": [False, 0x00004000],
            "fatal_fault": [False, 0x00008000],
            "startup_fault": [False, 0x00010000],
            "watchdog_timer_reset": [False, 0x00020000],
            "field_calibration": [False, 0x00040000],
            # ...
            "over_power": [False, 0x00100000],
            # Controller specific fault bits
            # ...
            "controller_checksum": [False, 0x40000000],
            "controller_status": [False, 0x80000000],
        }
    )

    source_on: bool = False
    source_power: float = 0.0


class SimulatedChtobisr(StateMachineDevice):
    """Class to simulate Coherent OBIS Laser Remote"""

    def _initialize_data(self) -> None:
        """Initialize the device's attributes."""
        self.connected = True

        self.lasers = {
            1: ChtobisrLaser(),
            2: ChtobisrLaser(),
            3: ChtobisrLaser(),
        }

    @has_log
    def backdoor_set_interlock(self, laser: int, value: str) -> None:
        """Sets interlock via backdoor"""
        if value not in ["ON", "OFF"]:
            self.log.error("Interlock can only be set to ON or OFF")
        else:
            self.lasers[laser].interlock = value

    def reset(self) -> None:
        """Resets all parameters by calling initialize function"""
        self._initialize_data()

    def build_status_code(self, laser: int) -> int:
        """ "
            Builds the device status code

        :return: status code
        """
        return build_code(self.lasers[laser].status)

    def build_fault_code(self, laser: int) -> int:
        """ "
            Builds the device fault code

        :return: fault code
        """
        return build_code(self.lasers[laser].faults)

    @has_log
    def backdoor_set_status(self, laser: int, statusname: str, value: bool) -> None:
        """Sets status code via backdoor
        :param statusname: name of status attribute
        :param value: true or false
        :return: none
        """
        try:
            self.lasers[laser].status[statusname][0] = value
        except KeyError as e:
            self.log.error(f"An error occurred: {e}")

    @has_log
    def backdoor_set_fault(self, laser: int, faultname: str, value: bool) -> None:
        """Sets fault code via backdoor
        :param faultname: name of fault attribute
        :param value: true or false
        :return: none
        """
        try:
            self.lasers[laser].faults[faultname][0] = value
        except KeyError as e:
            self.log.error(f"An error occurred: {e}")

    def backdoor_set_id(self, laser: int, id: str) -> None:
        self.lasers[laser].id = id

    def _get_state_handlers(self) -> dict[str, State]:
        return {
            "default": DefaultState(),
        }

    def _get_initial_state(self) -> str:
        return "default"

    def _get_transition_handlers(self) -> OrderedDict:
        return OrderedDict([])

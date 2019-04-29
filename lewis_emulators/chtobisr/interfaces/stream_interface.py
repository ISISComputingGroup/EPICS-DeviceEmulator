from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply


@has_log
class ChtobisrStreamInterface(StreamInterface):
    """
    Stream interface for the Coherent OBIS Laser Remote
    """

    commands = {
        CmdBuilder("get_id").escape("*IDN?").build(),
        CmdBuilder("set_reset").escape("*RST").build(),
        CmdBuilder("get_interlock").escape("SYSTEM:LOCK?").build(),
        CmdBuilder("get_status").escape("SYSTEM:STATUS?").build(),
        CmdBuilder("get_faults").escape("SYSTEM:FAULT?").build(),
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def handle_error(self, request, error):
        """
        If command is not recognised, print and error

        Args:
            request: requested string
            error: problem
        """

        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    @conditional_reply("connected")
    def get_id(self):
        """
        Gets the device Identification string

        :return:  Device ID string
        """

        return "{}".format(self._device.id)

    @conditional_reply("connected")
    def set_reset(self):
        """
        Resets the device

        :return:  none
        """

        self._device.reset()

    @conditional_reply("connected")
    def get_interlock(self):
        """
        Gets the device interlock status

        :return: Interlock status
        """

        return "{}".format(self._device.interlock)

    @conditional_reply("connected")
    def build_status_code(self):
        """"
        Builds the device status code

        :return: status code
        """
        status_code = 0x00000000

        # Laser specific status bits

        if self.status.laser_fault:
            status_code += 0x00000001

        if self.status.laser_emission:
            status_code += 0x00000002

        if self.status.laser_ready:
            status_code += 0x00000004

        if self.status.laser_standby:
            status_code += 0x00000008

        if self.status.cdrh_delay:
            status_code += 0x00000010

        if self.status.laser_hardware_fault:
            status_code += 0x00000020

        if self.status.laser_error:
            status_code += 0x00000040

        if self.status.laser_power_calibration:
            status_code += 0x00000080

        if self.status.laser_warm_up:
            status_code += 0x00000100

        if self.status.laser_noise:
            status_code += 0x00000200

        if self.status.external_operating_mode:
            status_code += 0x00000400

        if self.status.field_calibration:
            status_code += 0x00000800

        if self.status.laser_power_voltage:
            status_code += 0x00001000

        # Controller specific status bits

        if self.status.controller_standby:
            status_code += 0x02000000

        if self.status.controller_interlock:
            status_code += 0x04000000

        if self.status.controller_enumeration:
            status_code += 0x08000000

        if self.status.controller_error:
            status_code += 0x10000000

        if self.status.controller_fault:
            status_code += 0x20000000

        if self.status.remote_active:
            status_code += 0x40000000

        if self.status.controller_indicator:
            status_code += 0x80000000

        return status_code

    @conditional_reply("connected")
    def get_status(self):
        """
            Returns status code
        :return: status code
        """

        return self.build_status_code()

    @conditional_reply("connected")
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
        if self.faults["over_power"]:
            fault_code += 0x00100000

        # Controller specific fault bits
        if self.faults["controller_checksum"]:
            fault_code += 0x40000000
        if self.faults["controller_status"]:
            fault_code += 0x80000000

        return fault_code

    @conditional_reply("connected")
    def get_faults(self):
        """
            Returns faults code
        :return: Formatted fault code
        """
        return "{%8D}".format(self.build_fault_code())

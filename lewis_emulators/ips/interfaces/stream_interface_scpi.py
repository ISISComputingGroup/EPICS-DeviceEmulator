from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis.utils.command_builder import CmdBuilder

from lewis_emulators.ips.modes import Activity, Control

from ..device import amps_to_tesla, tesla_to_amps

MODE_MAPPING = {
    0: Activity.HOLD,
    1: Activity.TO_SETPOINT,
    2: Activity.TO_ZERO,
    4: Activity.CLAMP,
}

CONTROL_MODE_MAPPING = {
    0: Control.LOCAL_LOCKED,
    1: Control.REMOTE_LOCKED,
    2: Control.LOCAL_UNLOCKED,
    3: Control.REMOTE_UNLOCKED,
}

class DeviceUID:
    """
    Predefined UIDs for all devices attached to the iPS controller.
    """
    magnet_temperature_sensor = "MB1.T1"
    level_meter = "DB1.L1"
    magnet_supply = "GRPZ"
    temperature_sensor_10T = "DB8.T1"
    pressure_sensor_10T = "DB5.P1"
    

@has_log
class IpsStreamInterface(StreamInterface):
    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_version").escape("*IDN?").eos().build(),
        # CmdBuilder("set_comms_mode").escape("Q4").eos().build(),
        # CmdBuilder("get_status").escape("X").eos().build(),
        CmdBuilder("get_current").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:CURR").eos().build(),
        CmdBuilder("get_supply_voltage").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:VOLT").eos().build(),
        CmdBuilder("get_measured_current").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:RCUR").eos().build(),
        CmdBuilder("get_current_setpoint").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:CSET").eos().build(),
        CmdBuilder("get_current_sweep_rate").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:RCST").eos().build(),
        CmdBuilder("get_field").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:FLD").eos().build(),
        CmdBuilder("get_field_setpoint").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:FSET").eos().build(),
        CmdBuilder("get_field_sweep_rate").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:RFST").eos().build(),
        CmdBuilder("get_software_voltage_limit").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:VLIM").eos().build(),
        CmdBuilder("get_persistent_magnet_current").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:PCUR").eos().build(),
        # CmdBuilder("get_trip_current").escape("R17").eos().build(),
        CmdBuilder("get_persistent_magnet_field").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:PFLD").eos().build(),
        # CmdBuilder("get_trip_field").escape("R19").eos().build(),
        CmdBuilder("get_heater_current").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SHTC").eos().build(),
        # CmdBuilder("get_neg_current_limit").escape("R21").eos().build(),
        CmdBuilder("get_pos_current_limit").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:CLIM").eos().build(),
        CmdBuilder("get_lead_resistance").escape(f"READ:DEV:{DeviceUID.magnet_temperature_sensor}:TEMP:SIG:RES").eos().build(),
        CmdBuilder("get_magnet_inductance").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:IND").eos().build(),
#        CmdBuilder("set_control_mode")
#        .escape("C")
#        .arg("0|1|2|3", argument_mapping=int)
#        .eos()
#        .build(),
        # Legacy command 'A': 0=HOLD, 1=TO_SETPOINT, 2=TO_ZERO, 4=CLAMP
        # CmdBuilder("set_mode").escape("A").int().eos().build(),
        # New command 'SET:DEV:<UID>:ACTN:': HOLD=HOLD, RTOS=TO_SETPOINT, RTOZ=TO_ZERO, CLMP=CLAMP
        CmdBuilder("set_mode").escape(f"SET:DEV:{DeviceUID.magnet_supply}:ACTN:").string().eos().build(),
        CmdBuilder("set_current").escape(f"SET:DEV:{DeviceUID.magnet_supply}:PSU:CSET:").float().eos().build(),
        CmdBuilder("set_field").escape(f"SET:DEV:{DeviceUID.magnet_supply}:PSU:FSET").float().eos().build(),
        CmdBuilder("set_field_sweep_rate").escape(f"SET:DEV:{DeviceUID.magnet_supply}:PSU:RFST").float().eos().build(),
        CmdBuilder("set_sweep_mode").escape("M").int().eos().build(),
        CmdBuilder("set_heater_on").escape(f"SET:DEV:{DeviceUID.magnet_supply}:PSU:SIG:SWHT:ON").eos().build(),
        CmdBuilder("set_heater_off").escape(f"SET:DEV:{DeviceUID.magnet_supply}:PSU:SIG:SWHT:OFF").eos().build(),
    }

    in_terminator = "\n"
    out_terminator = "\n"

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(
            request, error.__class__.__name__, error
        )
        print(err_string)
        self.log.error(err_string)
        return err_string

    @staticmethod
    def get_version():
        """ get_version()
        The format of the reply is:
            IDN:OXFORD INSTRUMENTS:MERCURY dd:ss:ff
            Where:
                dd is the basic instrument type (iPS , iPS, Cryojet etc.)
                ss is the serial number of the main board
                ff is the firmware version of the instrument
        :return: Simulated identity string
        """
        return "IDN:OXFORD INSTRUMENTS:MERCURY IPS:simulated:0.0.0"

    def set_comms_mode(self):
        """This sets the terminator that the device wants, not implemented in emulator. Command does not reply.
        """

    def set_control_mode(self, mode):
        self.device.control = CONTROL_MODE_MAPPING[mode]
        return "C"

    def set_mode(self, mode):
        mode = int(mode)
        try:
            self.device.activity = MODE_MAPPING[mode]
        except KeyError:
            raise ValueError("Invalid mode specified")
        return "A"

    def get_status(self):
        resp = "X{x1}{x2}A{a}C{c}H{h}M{m1}{m2}P{p1}{p2}"

        def translate_activity():
            for k, v in MODE_MAPPING.items():
                if v == self.device.activity:
                    return k
            else:
                raise ValueError("Device was in invalid mode, can't construct status")

        def get_heater_status_number():
            if self.device.heater_on:
                return 1
            else:
                return 0 if self.device.magnet_current == 0 else 2

        def is_sweeping() -> bool:
            if self.device.activity == Activity.TO_SETPOINT:
                return self.device.current != self.device.current_setpoint
            elif self.device.activity == Activity.TO_ZERO:
                return self.device.current != 0
            else:
                return False

        statuses = {
            "x1": 1 if self.device.quenched else 0,
            "x2": 0,
            "a": translate_activity(),
            "c": 4 if self.device.quenched else 3,
            "h": get_heater_status_number(),
            "m1": self.device.sweep_mode,
            "m2": 1 if is_sweeping() else 0,
            "p1": 0,
            "p2": 0,
        }

        return resp.format(**statuses)

    def get_current_setpoint(self):
        return "STAT:DEV:GRPZ:PSU:SIG:CURR:{}:A".format(self.device.current_setpoint)

    def get_supply_voltage(self):
        return "STAT:DEV:GRPZ:PSU:SIG:VOLT:{}:V".format(self.device.get_voltage())

    def get_measured_current(self):
        return "STAT:DEV:GRPZ:PSU:SIG:RCUR:{}:A".format(self.device.measured_current)

    def get_current(self):
        """Gets the demand current of the PSU."""
        return "STAT:DEV:GRPZ:PSU:SIG:CURR:{}:A".format(self.device.current)

    def get_current_sweep_rate(self):
        # Unsure as to whether units are returned?
        return "STAT:DEV:GRPZ:PSU:SIG:RCST:{}".format(self.device.current_ramp_rate)

    def get_field(self):
        return "STAT:SET:DEV:GRPZ:PSU:SIG:FSET:{}:VALID".format(amps_to_tesla(self.device.current))

    def get_field_setpoint(self):
        return "STAT:DEV:GRPZ:PSU:SIG:FLD:{}:T".format(amps_to_tesla(self.device.current_setpoint))

    def get_field_sweep_rate(self):
        return "STAT:DEV:GRPZ:PSU:SIG:RFST:{}:T".format(amps_to_tesla(self.device.current_ramp_rate))

    def get_software_voltage_limit(self):
        return "STAT:DEV:GRPZ:PSU:VLIM:{}:V".format(self.device.voltage_limit)

    def get_persistent_magnet_current(self):
        return "STAT:DEV:GRPZ:PSU:SIG:PCUR:{}:A".format(self.device.magnet_current)

    # TBD
    def get_trip_current(self):
        return "R{}".format(self.device.trip_current)

    def get_persistent_magnet_field(self):
        return "STAT:DEV:GRPZ:PSU:SIG:PFLD:{}:T".format(amps_to_tesla(self.device.magnet_current))

    # TBD
    def get_trip_field(self):
        return "R{}".format(amps_to_tesla(self.device.trip_current))

    def get_heater_current(self):
        return "STAT:DEV:GRPZ:PSU:SHTC:{}:mA".format(self.device.heater_current)

    def get_neg_current_limit(self):
        return "R{}".format(self.device.neg_current_limit)

    def get_pos_current_limit(self):
        return "R{}".format(self.device.pos_current_limit)

    def get_lead_resistance(self):
        return "R{}".format(self.device.lead_resistance)

    def get_magnet_inductance(self):
        return "R{}".format(self.device.inductance)

    def set_current(self, current):
        self.device.current_setpoint = float(current)
        return f"STAT:SET:DEV:GRPZ:PSU:SIG:CSET:{current}:VALID"

    def set_field(self, current):
        self.device.current_setpoint = tesla_to_amps(float(current))
        return "J"

    def set_heater_on(self):
        self.device.set_heater_status(True)
        return "H"

    def set_heater_off(self):
        self.device.set_heater_status(False)
        return "H"

    def set_field_sweep_rate(self, tesla):
        self.device.current_ramp_rate = tesla_to_amps(float(tesla))
        return "T"

    def set_sweep_mode(self, mode):
        self.device.sweep_mode = int(mode)
        return "M"

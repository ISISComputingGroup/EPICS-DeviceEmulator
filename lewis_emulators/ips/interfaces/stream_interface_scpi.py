from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis.utils.command_builder import CmdBuilder

from lewis_emulators.ips.modes_scpi import Activity, Control

from ..device_scpi import amps_to_tesla, tesla_to_amps

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
    protocol = "ips_scpi"
    in_terminator = "\n"
    out_terminator = "\n"

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_version").escape("*IDN?").eos().build(),
        # CmdBuilder("set_comms_mode").escape("Q4").eos().build(),
        CmdBuilder("get_magnet_supply_status").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:STAT").eos().build(),
        CmdBuilder("get_mode").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:ACTN").eos().build(),
        CmdBuilder("get_current").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:CURR").eos().build(),
        CmdBuilder("get_supply_voltage").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:VOLT").eos().build(),
        CmdBuilder("get_measured_current").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:RCUR").eos().build(),
        CmdBuilder("get_current_setpoint").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:CSET").eos().build(),
        CmdBuilder("get_current_sweep_rate").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:RCST").eos().build(),
        CmdBuilder("get_field").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:FLD").eos().build(),
        CmdBuilder("get_field_setpoint").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:FSET").eos().build(),
        CmdBuilder("get_field_sweep_rate").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:RFST").eos().build(),
        CmdBuilder("get_software_voltage_limit").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:VLIM").eos().build(),
        CmdBuilder("get_persistent_magnet_current").escape(
            f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:PCUR").eos().build(),
        # CmdBuilder("get_trip_current").escape("R17").eos().build(),
        CmdBuilder("get_persistent_magnet_field").escape(
            f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:PFLD").eos().build(),
        # CmdBuilder("get_trip_field").escape("R19").eos().build(),
        CmdBuilder("get_heater_current").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SHTC").eos().build(),
        # CmdBuilder("get_neg_current_limit").escape("R21").eos().build(),
        CmdBuilder("get_pos_current_limit").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:CLIM").eos().build(),
        CmdBuilder("get_lead_resistance").escape(
            f"READ:DEV:{DeviceUID.magnet_temperature_sensor}:TEMP:SIG:RES").eos().build(),
        CmdBuilder("get_magnet_inductance").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:IND").eos().build(),
        CmdBuilder("get_heater_status").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:SIG:SWHT").eos().build(),
        CmdBuilder("get_bipolar_mode").escape(f"READ:DEV:{DeviceUID.magnet_supply}:PSU:BIPL").eos().build(),
        CmdBuilder("set_mode").escape(f"SET:DEV:{DeviceUID.magnet_supply}:ACTN:").string().eos().build(),
        CmdBuilder("set_current").escape(f"SET:DEV:{DeviceUID.magnet_supply}:PSU:SIG:CSET:").float().eos().build(),
        CmdBuilder("set_field").escape(f"SET:DEV:{DeviceUID.magnet_supply}:PSU:FSET").float().eos().build(),
        CmdBuilder("set_field_sweep_rate").escape(f"SET:DEV:{DeviceUID.magnet_supply}:PSU:RFST").float().eos().build(),
        CmdBuilder("set_heater_on").escape(f"SET:DEV:{DeviceUID.magnet_supply}:PSU:SIG:SWHT:ON").eos().build(),
        CmdBuilder("set_heater_off").escape(f"SET:DEV:{DeviceUID.magnet_supply}:PSU:SIG:SWHT:OFF").eos().build(),
        CmdBuilder("set_bipolar_mode").escape(f"SET:DEV:{DeviceUID.magnet_supply}:PSU:BIPL:").string().eos().build(),
    }

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

    def get_mode(self):
        return f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:ACTN:{self.device.activity.value}"

    def set_mode(self, mode):
        mode = int(mode)
        try:
            self.device.activity = MODE_MAPPING[mode]
        except KeyError:
            raise ValueError("Invalid mode specified")
        return "A"

    def get_magnet_supply_status(self):
        """
        The format of the reply is:
            STAT:DEV:{DeviceUID.magnet_supply}:PSU:STAT:00000000

            Where :
                | Status                               | Bit Value | Bit Position |
                |--------------------------------------|-----------|--------------|
                | Switch Heater Mismatch               | 00000001  | 0            |
                | Over Temperature [Rundown Resistors] | 00000002  | 1            |
                | Over Temperature [Sense Resistor]    | 00000004  | 2            |
                | Over Temperature [PCB]               | 00000008  | 3            |
                | Calibration Failure                  | 00000010  | 4            |
                | MSP430 Firmware Error                | 00000020  | 5            |
                | Rundown Resistors Failed             | 00000040  | 6            |
                | MSP430 RS-485 Failure                | 00000080  | 7            |
                | Quench detected                      | 00000100  | 8            |
                | Catch detected                       | 00000200  | 9            |
                | Over Temperature [Sense Amplifier]   | 00001000  | 12           |
                | Over Temperature [Amplifier 1]       | 00002000  | 13           |
                | Over Temperature [Amplifier 2]       | 00004000  | 14           |
                | PWM Cutoff                           | 00008000  | 15           |
                | Voltage ADC error                    | 00010000  | 16           |
                | Current ADC error                    | 00020000  | 17           |

            This information is not published and was derived from
            direct questions to Oxford Instruments.
        """
        resp = f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:STAT:{self.device.magnet_supply_status.value:08x}"
        return resp

    def get_current_setpoint(self):
        return f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:SIG:CURR:{self.device.current_setpoint}:A"

    def get_supply_voltage(self):
        return f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:SIG:VOLT:{self.device.get_voltage()}:V"

    def get_measured_current(self):
        return f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:SIG:RCUR:{self.device.measured_current}:A"

    def get_current(self):
        """Gets the demand current of the PSU."""
        return f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:SIG:CURR:{self.device.current}:A"

    def get_current_sweep_rate(self):
        # Unsure as to whether units are returned?
        return f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:SIG:RCST:{self.device.current_ramp_rate}"

    def get_field(self):
        return f"STAT:SET:DEV:{DeviceUID.magnet_supply}:PSU:SIG:FSET:{amps_to_tesla(self.device.current)}:VALID"

    def get_field_setpoint(self):
        return f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:SIG:FLD:{amps_to_tesla(self.device.current_setpoint)}:T"

    def get_field_sweep_rate(self):
        return f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:SIG:RFST:{amps_to_tesla(self.device.current_ramp_rate)}:T"

    def get_software_voltage_limit(self):
        return f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:VLIM:{self.device.voltage_limit}:V"

    def get_persistent_magnet_current(self):
        return f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:SIG:PCUR:{self.device.magnet_current}:A"

    # TBD
    def get_trip_current(self):
        return f"R{self.device.trip_current}"

    def get_persistent_magnet_field(self):
        return f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:SIG:PFLD:{amps_to_tesla(self.device.magnet_current)}:T"

    # TBD
    def get_trip_field(self):
        return f"R{amps_to_tesla(self.device.trip_current)}"

    def get_heater_current(self):
        return f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:SHTC:{self.device.heater_current}:mA"

    def get_neg_current_limit(self):
        ret = f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:CLIM:{self.device.neg_current_limit}:A"
        return ret

    def get_pos_current_limit(self):
        ret = f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:CLIM:{self.device.pos_current_limit}:A"
        return ret

    def get_lead_resistance(self):
        ret = f"STAT:DEV:{DeviceUID.magnet_temperature_sensor}:TEMP:SIG:RES:{self.device.lead_resistance}:Ohm"
        return ret

    def get_magnet_inductance(self):
        ret = f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:IND:{self.device.inductance}:H"
        return ret

    def get_heater_status(self):
        return f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:SIG:SWHT:{'ON' if self.device.heater_on else 'OFF'}"

    def get_bipolar_mode(self):
        return f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:BIPL:{'ON' if self.device.bipolar else 'OFF'}"

    def set_current(self, current):
        self.device.current_setpoint = float(current)
        return f"STAT:SET:DEV:{DeviceUID.magnet_supply}:PSU:SIG:CSET:{current}:VALID"

    def set_field(self, current):
        ret = f"STAT:SET:DEV:{DeviceUID.magnet_supply}:PSU:SIG:FLD:{f'amps_to_tesla(float(current)):.5f'}:VALID"
        self.device.current_setpoint = tesla_to_amps(float(current))
        return ret

    def set_heater_on(self):
        self.device.set_heater_status(True)
        ret = f"STAT:SET:DEV:{DeviceUID.magnet_supply}:PSU:SIG:SWHT:ON:VALID"
        return ret

    def set_heater_off(self):
        self.device.set_heater_status(False)
        ret = f"STAT:SET:DEV:{DeviceUID.magnet_supply}:PSU:SIG:SWHT:OFF:VALID"
        return ret

    def set_field_sweep_rate(self, tesla):
        self.device.current_ramp_rate = tesla_to_amps(float(tesla))
        ret = f"STAT:SET:DEV:{DeviceUID.magnet_supply}:PSU:RFST:{f'tesla:.3f'}:VALID"
        return ret

    def set_bipolar_mode(self, mode):
        self.device.bipolar = bool(mode)
        print(f"set_bipolar(): mode = {mode}")
        return f"STAT:DEV:{DeviceUID.magnet_supply}:PSU:BIPL:{'ON' if self.device.bipolar else 'OFF'}"

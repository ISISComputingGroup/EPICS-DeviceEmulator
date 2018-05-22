from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from ..device import amps_to_tesla, tesla_to_amps


@has_log
class IpsStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_version").escape("V").eos().build(),
        CmdBuilder("set_comms_mode").escape("Q4").eos().build(),
        CmdBuilder("get_status").escape("X").eos().build(),
        CmdBuilder("get_current").escape("R0").eos().build(),
        CmdBuilder("get_supply_voltage").escape("R1").eos().build(),
        CmdBuilder("get_measured_current").escape("R2").eos().build(),
        CmdBuilder("get_current_setpoint").escape("R5").eos().build(),
        CmdBuilder("get_current_sweep_rate").escape("R6").eos().build(),
        CmdBuilder("get_field").escape("R7").eos().build(),
        CmdBuilder("get_field_setpoint").escape("R8").eos().build(),
        CmdBuilder("get_field_sweep_rate").escape("R9").eos().build(),
        CmdBuilder("get_software_voltage_limit").escape("R15").eos().build(),
        CmdBuilder("get_persistent_magnet_current").escape("R16").eos().build(),
        CmdBuilder("get_trip_current").escape("R17").eos().build(),
        CmdBuilder("get_persistent_magnet_field").escape("R18").eos().build(),
        CmdBuilder("get_trip_field").escape("R19").eos().build(),
        CmdBuilder("get_heater_current").escape("R20").eos().build(),
        CmdBuilder("get_neg_current_limit").escape("R21").eos().build(),
        CmdBuilder("get_pos_current_limit").escape("R22").eos().build(),
        CmdBuilder("get_lead_resistance").escape("R23").eos().build(),
        CmdBuilder("get_magnet_inductance").escape("R24").eos().build(),

        CmdBuilder("set_control_mode").escape("C").int().eos().build(),
        CmdBuilder("set_mode").escape("A").int().eos().build(),
        CmdBuilder("set_current").escape("I").float().eos().build(),
        CmdBuilder("set_field").escape("J").float().eos().build(),

        CmdBuilder("set_heater_on").escape("H1").eos().build(),
        CmdBuilder("set_heater_off").escape("H0").eos().build(),
        CmdBuilder("set_heater_off").escape("H2").eos().build(),
    }

    in_terminator = "\r"
    out_terminator = "\r"

    def handle_error(self, request, error):
        err_string = "command was: {}, error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    def get_version(self):
        return "Simulated IPS"

    def set_comms_mode(self):
        """
        This sets the terminator that the device wants, not implemented in emulator. Command does not reply.
        """

    def set_control_mode(self, mode):
        return "C"

    def set_mode(self, mode):
        #  TODO: This command?
        return "A"

    def get_status(self):
        resp = "X{x1}{x2}A{a}C{c}H{h}M{m1}{m2}P{p1}{p2}"

        statuses = {
            "x1": 0,
            "x2": 0,
            "a": 0,
            "c": 3,
            "h": 1 if self.device.heater_on else 0,
            "m1": 1,
            "m2": 0,
            "p1": 0,
            "p2": 0,
        }

        return resp.format(**statuses)

    def get_current_setpoint(self): 
        return "R{}".format(self.device.current_setpoint)

    def get_supply_voltage(self): 
        return "R{}".format(self.device.voltage)

    def get_measured_current(self):
        return "R{}".format(self.device.measured_current)

    def get_current(self): 
        return "R{}".format(self.device.current)

    def get_current_sweep_rate(self): 
        return "R{}".format(self.device.current_sweep_rate)

    def get_field(self):
        return "R{}".format(amps_to_tesla(self.device.current))

    def get_field_setpoint(self): 
        return "R{}".format(amps_to_tesla(self.device.current_setpoint))

    def get_field_sweep_rate(self): 
        return "R{}".format(amps_to_tesla(self.device.current_sweep_rate))

    def get_software_voltage_limit(self): 
        return "R0"

    def get_persistent_magnet_current(self): 
        return "R{}".format(self.device.magnet_current)

    def get_trip_current(self): 
        return "R{}".format(self.device.trip_current)

    def get_persistent_magnet_field(self): 
        return "R{}".format(amps_to_tesla(self.device.magnet_current))

    def get_trip_field(self): 
        return "R{}".format(amps_to_tesla(self.device.trip_current))

    def get_heater_current(self): 
        return "R{}".format(self.device.heater_current)

    def get_neg_current_limit(self): 
        return "R0"

    def get_pos_current_limit(self): 
        return "R0"

    def get_lead_resistance(self): 
        return "R{}".format(self.device.lead_resistance)

    def get_magnet_inductance(self): 
        return "R0"

    def set_current(self, current):
        self.device.current_setpoint = float(current)
        return "I"

    def set_field(self, current):
        self.device.current_setpoint = tesla_to_amps(float(current))
        return "J"

    def set_heater_on(self):
        self.device.set_heater_status(True)
        return "H"

    def set_heater_off(self):
        self.device.set_heater_status(False)
        return "H"

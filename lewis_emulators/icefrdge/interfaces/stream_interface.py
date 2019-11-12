from lewis.adapters.stream import StreamInterface, Cmd
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis_emulators.utils.constants import ACK, ENQ


@has_log
class IceFridgeStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("set_auto_temp_setpoint").escape("AUTO TSET=").float().eos().build(),
        CmdBuilder("get_auto_temp_set_RBV").escape("AUTO TSET?").eos().build(),
        CmdBuilder("get_auto_temp_set_RBV").escape("AUTO TEMP?").eos().build(),

        CmdBuilder("set_manual_temp_setpoint").escape("MANUAL TSET=").float().eos().build(),
        CmdBuilder("get_manual_temp_set_RBV").escape("MANUAL TSET?").eos().build(),
        CmdBuilder("get_manual_temp_set_RBV").escape("MANUAL TEMP?").eos().build(),

        CmdBuilder("get_cryo_temps").escape("CRYO-TEMPS?").eos().build(),

        CmdBuilder("set_loop_temp_setpoint").escape("CRYO-TSET=").int().escape(",").float().eos().build(),
        CmdBuilder("get_loop_temp").escape("CRYO-TSET").int().escape("?").eos().build(),

        CmdBuilder("set_loop_proportional_setpoint").escape("CRYO-P=").int().escape(",").float().eos().build(),
        CmdBuilder("get_loop_proportional").escape("CRYO-P").int().escape("?").eos().build(),

        CmdBuilder("set_loop_integral_setpoint").escape("CRYO-I=").int().escape(",").float().eos().build(),
        CmdBuilder("get_loop_integral").escape("CRYO-I").int().escape("?").eos().build(),

        CmdBuilder("set_loop_derivative_setpoint").escape("CRYO-D=").int().escape(",").float().eos().build(),
        CmdBuilder("get_loop_derivative").escape("CRYO-D").int().escape("?").eos().build(),

        CmdBuilder("set_loop_ramp_rate_setpoint").escape("CRYO-RAMP=").int().escape(",").float().eos().build(),
        CmdBuilder("get_loop_ramp_rate").escape("CRYO-RAMP").int().escape("?").eos().build(),

        CmdBuilder("get_mc_cernox").escape("LS-DIRECT-READ=RDGK? 4").eos().build(),
        CmdBuilder("get_mc_ruo").escape("LS-DIRECT-READ=RDGK? 6").eos().build(),
        CmdBuilder("get_still_temp").escape("STILL?").eos().build(),

        CmdBuilder("set_mc_temp_setpoint").escape("LS-DIRECT-SET=SETP ").float().eos().build(),
        CmdBuilder("get_mc_temp_setpoint").escape("LS-DIRECT-READ=SETP?").eos().build(),

        CmdBuilder("set_lakeshore_cmode").escape("LS-DIRECT-SET=CMODE ").int().eos().build(),
        CmdBuilder("set_lakeshore_scan").escape("LS-DIRECT-SET=SCAN 6,").int().eos().build(),

        CmdBuilder("set_lakeshore_mc_PIDs").escape("LS-DIRECT-SET=PID ").float().escape(",").float().escape(",").float(
            ).eos().build(),
        CmdBuilder("get_lakeshore_mc_PIDs").escape("LS-DIRECT-READ=PID?").eos().build(),

        CmdBuilder("set_lakeshore_cset").escape("LS-DIRECT-SET=CSET 06,0,1,025,1,").int().escape(",+388.000").eos(
            ).build(),
        CmdBuilder("set_lakeshore_mc_heater_range").escape("LS-DIRECT-SET=HTRRNG ").int().eos().build(),
        CmdBuilder("get_lakeshore_mc_heater_range").escape("LS-DIRECT-READ=HTRRNG?").eos().build(),

        CmdBuilder("get_lakeshore_mc_heater_percentage").escape("LS-DIRECT-READ=HTR?").eos().build(),
        CmdBuilder("get_lakeshore_still_output").escape("LS-DIRECT-READ=STILL?").eos().build(),

        CmdBuilder("get_lakeshore_channel_voltage_range").escape("LS-DIRECT-READ=RDGRNG? ").int().eos().build(),
        CmdBuilder("set_lakeshore_channel_voltage_range").escape("LS-DIRECT-SET=RDGRNG ").int().escape(",").int(
            ).escape(",").int().escape(",").int().escape(",").int().escape(",").int().eos().build(),

        CmdBuilder("get_mimic_pressures").escape("P?").eos().build(),

        CmdBuilder("get_mimic_valves").escape("VALVES?").eos().build(),
        CmdBuilder("set_mimic_valve").escape("V").int().escape("=").int().eos().build()
    }

    in_terminator = "\n"
    out_terminator = "\n"

    def handle_error(self, request, error):
        """
        Prints and logs an error message if a command is not recognised.

        Args:
            request : Request.
            error: The error that has occurred.
        Returns:
            String: The error string.
        """
        err_string = "command was: \"{}\", error was: {}: {}\n".format(request, error.__class__.__name__, error)
        print(err_string)
        self.log.error(err_string)
        return err_string

    def set_auto_temp_setpoint(self, temp_setpoint):
        self._device.auto_temp_setpoint = temp_setpoint

    def get_auto_temp_set_RBV(self):
        return self._device.auto_temp_setpoint

    def set_manual_temp_setpoint(self, temp_setpoint):
        self._device.manual_temp_setpoint = temp_setpoint

    def get_manual_temp_set_RBV(self):
        return self._device.manual_temp_setpoint

    def get_cryo_temps(self):
        return "CRYO-TEMPS={},{},{},{}".format(self._device.vti_temp1, self._device.vti_temp2, self._device.vti_temp3,
                                               self._device.vti_temp4)

    def set_loop_temp_setpoint(self, loop_num, temp_setpoint):
        self._device.vti_loop_channels[loop_num].vti_loop_temp_setpoint = temp_setpoint

    def get_loop_temp(self, loop_num):
        return "CRYO-TSET{}={}".format(loop_num, self._device.vti_loop_channels[loop_num].vti_loop_temp_setpoint)

    def set_loop_proportional_setpoint(self, loop_num, proportional_setpoint):
        self._device.vti_loop_channels[loop_num].vti_loop_proportional = proportional_setpoint

    def get_loop_proportional(self, loop_num):
        return "CRYO-P{}={}".format(loop_num, self._device.vti_loop_channels[loop_num].vti_loop_proportional)

    def set_loop_integral_setpoint(self, loop_num, integral_setpoint):
        self._device.vti_loop_channels[loop_num].vti_loop_integral = integral_setpoint

    def get_loop_integral(self, loop_num):
        return "CRYO-I{}={}".format(loop_num, self._device.vti_loop_channels[loop_num].vti_loop_integral)

    def set_loop_derivative_setpoint(self, loop_num, derivative_setpoint):
        self._device.vti_loop_channels[loop_num].vti_loop_derivative = derivative_setpoint

    def get_loop_derivative(self, loop_num):
        return "CRYO-D{}={}".format(loop_num, self._device.vti_loop_channels[loop_num].vti_loop_derivative)

    def set_loop_ramp_rate_setpoint(self, loop_num, ramp_rate_setpoint):
        self._device.vti_loop_channels[loop_num].vti_loop_ramp_rate = ramp_rate_setpoint

    def get_loop_ramp_rate(self, loop_num):
        return "CRYO-RAMP{}={}".format(loop_num, self._device.vti_loop_channels[loop_num].vti_loop_ramp_rate)

    def get_mc_cernox(self):
        return self._device.lakeshore_mc_cernox

    def get_mc_ruo(self):
        return self._device.lakeshore_mc_ruo

    def get_still_temp(self):
        return "STILL={}".format(self._device.lakeshore_still_temp)

    def set_mc_temp_setpoint(self, temp_setpoint):
        self.device.lakeshore_mc_temp_setpoint = temp_setpoint

    def get_mc_temp_setpoint(self):
        return self.device.lakeshore_mc_temp_setpoint

    def set_lakeshore_scan(self, scan_num):
        self.device.lakeshore_scan = scan_num

    def set_lakeshore_cmode(self, cmode):
        self.device.lakeshore_cmode = cmode

    def set_lakeshore_mc_PIDs(self, proportional, integral, derivative):
        self.device.lakeshore_mc_proportional = proportional
        self.device.lakeshore_mc_integral = integral
        self.device.lakeshore_mc_derivative = derivative

    def get_lakeshore_mc_PIDs(self):
        return "{},{},{}".format(self.device.lakeshore_mc_proportional, self.device.lakeshore_mc_integral,
                                 self.device.lakeshore_mc_derivative)

    def set_lakeshore_cset(self, cset_heater_range):
        # The old SECI LabView software sent a two messages when you set the heater range set point. One was an
        # LS-DIRECT-SET=CSET command and the other was LS-DIRECT-SET=HTRRNG. This method corresponds to the first
        # command, which sent a bunch of numbers that we are not dealing with in this IOC and the heater range.
        # Therefore, we only have field in the device emulator for testing the values sent in both commands, and in
        # here we just set the device heater range to the argument.
        self.device.lakeshore_mc_heater_range = cset_heater_range

    def set_lakeshore_mc_heater_range(self, heater_range):
        # The old SECI LabView software sent a two messages when you set the heater range set point. One was an
        # LS-DIRECT-SET=CSET command and the other was LS-DIRECT-SET=HTRRNG. This method corresponds to the second
        # command, which is the actual command for setting the heater range of the dilution fridge. Since the first
        # command should have been sent already, and thus the device emulator heater range should already have the
        # same value as the given range, we just check if that value is already the same and throw an error if that is
        # not the case.
        if heater_range != self.device.lakeshore_mc_heater_range:
            raise ValueError("Invalid command sequence! The heater range should have already been set to the new value "
                             "by a CSET command!")

    def get_lakeshore_mc_heater_range(self):
        return self.device.lakeshore_mc_heater_range

    def get_lakeshore_mc_heater_percentage(self):
        return self.device.lakeshore_mc_heater_percentage

    def get_lakeshore_still_output(self):
        return self.device.lakeshore_still_output

    def get_lakeshore_channel_voltage_range(self, channel):
        if channel == 5:
            return "{},{:02d},{:02d},{},{}".format(0, self.device.lakeshore_exc_voltage_range_ch5, 1, 2, 3)
        elif channel == 6:
            return "{},{:02d},{:02d},{},{}".format(0, self.device.lakeshore_exc_voltage_range_ch6, 1, 2, 3)
        else:
            raise ValueError("channel number can only be either 5 or 6!")

    def set_lakeshore_channel_voltage_range(self, channel, mode, voltage_range, resistance_range, auto_range_mode,
                                            excitation_mode):
        if mode != 0:
            raise ValueError("mode should always be 0")

        if resistance_range != 1:
            raise ValueError("resistance_range value should always be 1!")

        if auto_range_mode != 2:
            raise ValueError("auto_range_mode value should always be 2!")

        if excitation_mode != 3:
            raise ValueError("excitation_mode value should always be 3!")

        if channel == 5:
            self.device.lakeshore_exc_voltage_range_ch5 = voltage_range
        elif channel == 6:
            self.device.lakeshore_exc_voltage_range_ch6 = voltage_range
        else:
            raise ValueError("channel number can only be either 5 or 6!")

    def get_mimic_pressures(self):
        return "P1={:f},P2={:f},P3={:f},P4={:f}".format(self.device.mimic_pressures[0], self.device.mimic_pressures[1],
                                                        self.device.mimic_pressures[2], self.device.mimic_pressures[3])

    def get_mimic_valves(self):
        valve_statuses = []
        for i in range(10):
            valve_statuses.append("V{}={},".format(i + 1, IceFridgeStreamInterface._bool_to_int(
                self.device.mimic_valves[i])))

        valve_reply = "".join(valve_statuses)
        valve_reply = valve_reply[:-1]

        print(valve_reply)
        return valve_reply

    def set_mimic_valve(self, valve_number, valve_status):
        self.device.set_mimic_valve(valve_number, valve_status)

    @staticmethod
    def _bool_to_int(boolean):
        if boolean:
            return 1
        else:
            return 0

from lewis.adapters.stream import StreamInterface, Cmd

from lewis_emulators.icefrdge import SimulatedIceFridge
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis_emulators.utils.constants import ACK, ENQ
from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")

@has_log
class IceFridgeStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
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

        CmdBuilder("get_pressures").escape("P?").eos().build(),

        CmdBuilder("set_valve").escape("V").int().escape("=").int().eos().build(),
        CmdBuilder("set_solenoid_valve").escape("SV").int().escape("=").int().eos().build(),
        CmdBuilder("get_valves").escape("VALVES?").eos().build(),

        CmdBuilder("set_proportional_valve").escape("PV").int().escape("=").float().eos().build(),
        CmdBuilder("set_needle_valve").escape("NV=").float().eos().build(),
        CmdBuilder("get_proportional_valves").escape("PV?").eos().build(),

        CmdBuilder("get_1K_stage").escape("CRYO?").eos().build(),
        CmdBuilder("get_mc_temp").escape("MC?").eos().build(),
        CmdBuilder("get_mc_resistance").escape("MC-R?").eos().build(),

        CmdBuilder("set_skipped_status").escape("SKIP").eos().build(),
        CmdBuilder("set_stopped_status").escape("STOP").eos().build(),

        CmdBuilder("set_condense").escape("CONDENSE").eos().build(),
        CmdBuilder("set_circulate").escape("CIRCULATE").eos().build(),
        CmdBuilder("set_temp_control").escape("TSET=").float().eos().build(),
        CmdBuilder("get_temp_control").escape("TSET?").eos().build(),
        CmdBuilder("set_make_safe").escape("MAKE SAFE").eos().build(),
        CmdBuilder("set_warm_up").escape("WARM UP").eos().build(),

        CmdBuilder("get_mimic_info").escape("INFO?").eos().build(),
        CmdBuilder("get_state").escape("STATE?").eos().build(),

        CmdBuilder("set_nv_mode").escape("NVMODE=").string().eos().build(),
        CmdBuilder("get_nv_mode").escape("NVMODE?").eos().build(),

        CmdBuilder("set_1k_pump").escape("1KPUMP=").int().eos().build(),
        CmdBuilder("get_pumps").escape("PUMPS?").eos().build(),
        CmdBuilder("set_he3_pump").escape("HE3PUMP=").int().eos().build(),
        CmdBuilder("set_roots_pump").escape("ROOTS=").int().eos().build()
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

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

    @if_connected
    def get_cryo_temps(self):
        return "CRYO-TEMPS={},{},{},{}".format(self._device.vti_temps[0], self._device.vti_temps[1],
                                               self._device.vti_temps[2], self._device.vti_temps[3])

    @if_connected
    def set_loop_temp_setpoint(self, loop_num, temp_setpoint):
        self._device.vti_loop_channels[loop_num].vti_loop_temp_setpoint = temp_setpoint
        return "OK"

    @if_connected
    def get_loop_temp(self, loop_num):
        return "CRYO-TSET{}={}".format(loop_num, self._device.vti_loop_channels[loop_num].vti_loop_temp_setpoint)

    @if_connected
    def set_loop_proportional_setpoint(self, loop_num, proportional_setpoint):
        self._device.vti_loop_channels[loop_num].vti_loop_proportional = proportional_setpoint
        return "OK"

    @if_connected
    def get_loop_proportional(self, loop_num):
        return "CRYO-P{}={}".format(loop_num, self._device.vti_loop_channels[loop_num].vti_loop_proportional)

    @if_connected
    def set_loop_integral_setpoint(self, loop_num, integral_setpoint):
        self._device.vti_loop_channels[loop_num].vti_loop_integral = integral_setpoint
        return "OK"

    @if_connected
    def get_loop_integral(self, loop_num):
        return "CRYO-I{}={}".format(loop_num, self._device.vti_loop_channels[loop_num].vti_loop_integral)

    @if_connected
    def set_loop_derivative_setpoint(self, loop_num, derivative_setpoint):
        self._device.vti_loop_channels[loop_num].vti_loop_derivative = derivative_setpoint
        return "OK"

    @if_connected
    def get_loop_derivative(self, loop_num):
        return "CRYO-D{}={}".format(loop_num, self._device.vti_loop_channels[loop_num].vti_loop_derivative)

    @if_connected
    def set_loop_ramp_rate_setpoint(self, loop_num, ramp_rate_setpoint):
        self._device.vti_loop_channels[loop_num].vti_loop_ramp_rate = ramp_rate_setpoint
        return "OK"

    @if_connected
    def get_loop_ramp_rate(self, loop_num):
        return "CRYO-RAMP{}={}".format(loop_num, self._device.vti_loop_channels[loop_num].vti_loop_ramp_rate)

    @if_connected
    def get_mc_cernox(self):
        return self._device.lakeshore_mc_cernox

    @if_connected
    def get_mc_ruo(self):
        return self._device.lakeshore_mc_ruo

    @if_connected
    def get_still_temp(self):
        return "STILL={}".format(self._device.lakeshore_still_temp)

    @if_connected
    def set_mc_temp_setpoint(self, temp_setpoint):
        self.device.lakeshore_mc_temp_setpoint = temp_setpoint
        return "Set LakeShore 370"

    @if_connected
    def get_mc_temp_setpoint(self):
        return self.device.lakeshore_mc_temp_setpoint

    @if_connected
    def set_lakeshore_scan(self, scan_num):
        self.device.lakeshore_scan = scan_num
        return "Set LakeShore 370"

    @if_connected
    def set_lakeshore_cmode(self, cmode):
        self.device.lakeshore_cmode = cmode
        return "Set LakeShore 370"

    @if_connected
    def set_lakeshore_mc_PIDs(self, proportional, integral, derivative):
        self.device.lakeshore_mc_proportional = proportional
        self.device.lakeshore_mc_integral = integral
        self.device.lakeshore_mc_derivative = derivative
        return "Set LakeShore 370"

    @if_connected
    def get_lakeshore_mc_PIDs(self):
        return "{},{},{}".format(self.device.lakeshore_mc_proportional, self.device.lakeshore_mc_integral,
                                 self.device.lakeshore_mc_derivative)

    @if_connected
    def set_lakeshore_cset(self, cset_heater_range):
        # The old SECI LabView software sent a two messages when you set the heater range set point. One was an
        # LS-DIRECT-SET=CSET command and the other was LS-DIRECT-SET=HTRRNG. This method corresponds to the first
        # command, which sent a bunch of numbers that we are not dealing with in this IOC and the heater range.
        # Therefore, we only have field in the device emulator for testing the values sent in both commands, and in
        # here we just set the device heater range to the argument.
        self.device.lakeshore_mc_heater_range = cset_heater_range
        return "Set LakeShore 370"

    @if_connected
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
        return "Set LakeShore 370"

    @if_connected
    def get_lakeshore_mc_heater_range(self):
        return self.device.lakeshore_mc_heater_range

    @if_connected
    def get_lakeshore_mc_heater_percentage(self):
        return self.device.lakeshore_mc_heater_percentage

    @if_connected
    def get_lakeshore_still_output(self):
        return self.device.lakeshore_still_output

    @if_connected
    def get_lakeshore_channel_voltage_range(self, channel):
        if channel == 5:
            return "{},{:02d},{:02d},{},{}".format(0, self.device.lakeshore_exc_voltage_range_ch5, 1, 2, 3)
        elif channel == 6:
            return "{},{:02d},{:02d},{},{}".format(0, self.device.lakeshore_exc_voltage_range_ch6, 1, 2, 3)
        else:
            raise ValueError("channel number can only be either 5 or 6!")

    @if_connected
    def set_lakeshore_channel_voltage_range(self, channel, mode, voltage_range, resistance_range, auto_range_mode,
                                            excitation_mode):
        # The command to set the voltage range of a channel also returns 4 other values that are needed for the command
        # to get the voltage range. We check if the those 4 values correspond to the default values, as described in
        # the Lakeshore 370 manual.

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
            return "Set LakeShore 370"
        elif channel == 6:
            self.device.lakeshore_exc_voltage_range_ch6 = voltage_range
            return "Set LakeShore 370"
        else:
            raise ValueError("channel number can only be either 5 or 6!")

    @if_connected
    def get_pressures(self):
        return "P1={:f},P2={:f},P3={:f},P4={:f}".format(self.device.pressures[0], self.device.pressures[1],
                                                        self.device.pressures[2], self.device.pressures[3])

    @if_connected
    def set_valve(self, valve_number, valve_status):
        """
        Sets the status of a mimic valve in the mimic valve status list to a new value.
        :param valve_number: the index of the valve you want to set, from 1 to 10.
        :param valve_status: 1 if the valve is open, 0 if it is closed.
        :return: None
        """

        if IceFridgeStreamInterface._is_bit(valve_status):
            self.device.valves[valve_number - 1] = valve_status
            return "OK"
        else:
            raise ValueError("The status of the valve can be either 0 or 1!")

    @if_connected
    def set_solenoid_valve(self, valve_number, valve_status):
        """
        Sets the status of a mimic solenoid valve in the mimic solenoid valve status list to a new value.
        :param valve_number: the index of the valve you want to set, from 1 to 10.
        :param valve_status: 1 if the valve is open, 0 if it is closed.
        :return: None
        """

        if IceFridgeStreamInterface._is_bit(valve_status):
            self.device.solenoid_valves[valve_number - 1] = valve_status
            return "OK"
        else:
            raise ValueError("The status of the solenoid valve can be either 0 or 1!")

    @if_connected
    def get_valves(self):
        # the device response has 10 valve values in one string, so it is easier to build the string as a list
        # comprehension rather than doing it manually.
        valve_statuses = ["V{}={},".format(i + 1, self.device.valves[i]) for i in range(10)]

        valve_reply = "".join(valve_statuses)

        # the last element that was added was 'V10=x,' and we do not need a comma at the end of the message, so we
        # remove the last element
        valve_reply = valve_reply[:-1]

        solenoid_valves = "SV1={},SV2={},".format(self.device.solenoid_valves[0], self.device.solenoid_valves[1])

        valve_reply = solenoid_valves + valve_reply

        return valve_reply

    @staticmethod
    def _is_bit(number):
        if number == 0 or number == 1:
            return True
        else:
            return False

    @if_connected
    def set_proportional_valve(self, valve_num, valve_value):
        """
        Sets the status of a mimic valve in the mimic valve status list to a new value.
        :param valve_num: the index of the valve you want to set, which is 1, 2 or 4. This is because in the LabView
        software used on SECI, the mimic panel only has proportional valves 1, 2 and 4.
        :param valve_value: the new value of the valve.
        :return: None
        """

        if valve_num != 1 and valve_num != 2 and valve_num != 4:
            raise ValueError("valve number argument can only be 1, 2 or 4!")

        if valve_num == 4:
            valve_num = 3

        self.device.proportional_valves[valve_num - 1] = valve_value
        return "OK"

    @if_connected
    def get_proportional_valves(self):
        return "PV1={:f},PV2={:f},NV={:f},PV4={:f}".format(self.device.proportional_valves[0],
                                                           self.device.proportional_valves[1],
                                                           self.device.needle_valve,
                                                           self.device.proportional_valves[2])

    @if_connected
    def set_needle_valve(self, valve_value):
        self.device.needle_valve = valve_value
        return "OK"

    @if_connected
    def get_1K_stage(self):
        return "CRYO={:f}".format(self.device.temp_1K_stage)

    @if_connected
    def get_mc_temp(self):
        return "MC={:f}".format(self.device.mixing_chamber_temp)

    @if_connected
    def get_mc_resistance(self):
        return "MC-R={:f}".format(self.device.mixing_chamber_resistance)

    def set_skipped_status(self):
        self.device.skipped = True
        return "OK"

    def set_stopped_status(self):
        self.device.stopped = True
        return "OK"

    def set_condense(self):
        self.device.condense = True
        return "OK"

    def set_circulate(self):
        self.device.circulate = True
        return "OK"

    def set_temp_control(self, temperature):
        self.device.temp_control = temperature
        return "OK"

    def get_temp_control(self):
        return "TSET={}".format(self.device.temp_control)

    def set_make_safe(self):
        self.device.make_safe = True
        return "OK"

    def set_warm_up(self):
        self.device.warm_up = True
        return "OK"

    @if_connected
    def get_mimic_info(self):
        return self.device.mimic_info

    @if_connected
    def get_state(self):
        return self.device.state

    @if_connected
    def set_nv_mode(self, nv_mode):
        if nv_mode == "MANUAL":
            self.device.needle_valve_mode = False
            return "OK"
        elif nv_mode == "AUTO":
            self.device.needle_valve_mode = True
            return "OK"
        else:
            raise ValueError("nv mode can only be set to MANUAL or AUTO!")

    @if_connected
    def get_nv_mode(self):
        if self.device.needle_valve_mode:
            return "AUTO"
        else:
            return "MANUAL"

    @if_connected
    def set_1k_pump(self, pump_1k):
        if IceFridgeStreamInterface._is_bit(pump_1k):
            self.device.pump_1K = pump_1k
            return "OK"
        else:
            raise ValueError("1K pump value can be 1 or 0!")

    @if_connected
    def get_pumps(self):
        return "1KPUMP={},HE3PUMP={},ROOTS={}".format(IceFridgeStreamInterface._bit_to_pump_status(self.device.pump_1K),
                                                      IceFridgeStreamInterface._bit_to_pump_status(self.device.he3_pump),
                                                      IceFridgeStreamInterface._bit_to_pump_status(
                                                          self.device.roots_pump))

    @if_connected
    def set_he3_pump(self, he3_pump):
        if IceFridgeStreamInterface._is_bit(he3_pump):
            self.device.he3_pump = he3_pump
            return "OK"
        else:
            raise ValueError("Helium 3 pump value can be 1 or 0!")

    @if_connected
    def set_roots_pump(self, roots_pump):
        if IceFridgeStreamInterface._is_bit(roots_pump):
            self.device.roots_pump = roots_pump
            return "OK"
        else:
            raise ValueError("Roots pump value can be 1 or 0!")

    @staticmethod
    def _bit_to_pump_status(bit):
        if bit == 1:
            return "ON"
        elif bit == 0:
            return "OFF"
        else:
            raise ValueError("pump value in device can only be o or 1")

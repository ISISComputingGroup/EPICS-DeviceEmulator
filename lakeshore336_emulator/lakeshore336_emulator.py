import sys, random
sys.path.append("../test_framework")

from telnet_engine import TelnetEngine

class LakeshoreInput:
    def __init__(self):
        self.name = "Default Name"
        self._temperature = 0.0
        self.raw_voltage = random.uniform(0, 1000)
        self.has_high_alarm = False
        self.has_low_alarm = False
        self.alarm_enabled = True
        self.alarm_high_setpoint = 1000.0
        self.alarm_low_setpoint = 10.0
        self.alarm_deadband = 0.5
        self.alarm_latching = False
        self.alarm_audible = True
        self.alarm_visible = True
        self.reading_status = 0
        self.curve_number = 15
        self.sensor_type = 3
        self.autorange_on = True
        self.range = 5
        self.compensation_on = True
        self.units = 1


    def get_temperature(self):
        return_value = self._temperature;
        self._temperature += 0.1
        return return_value


class LakeshoreOutput:
    def __init__(self):
        self.temp_setpoint = 100.0
        self.ramp_on = True
        self.ramp_rate = 2.0


class CalibrationCurve:
    def __init__(self):
        self.name = "Emulator curve " # Must be 15 chars
        self.serial = "0123456789" # Must be 10 chars
        self.format = 1
        self.limit = 1000.0
        self.coeff = 2

class GetIdCommand:
    def __init__(self, emulator):
        self.id = "*IDN?"
        self._emu = emulator

    def execute_and_reply(self, data):
        return "LSCI,%s" % (self._emu.id)

class GetInputNameCommand:
    def __init__(self, emulator):
        self.id = "INNAME?"
        self._emu = emulator

    def execute_and_reply(self, data):
        return self._emu.get_target_input(data).name

class SetInputNameCommand:
    def __init__(self, emulator):
        self.id = "INNAME"
        self._emu = emulator

    def execute_and_reply(self, data):
        tokens = self._emu.get_set_tokens(data, self.id)
        index = tokens[0]
        new_name = tokens[1].strip("\"")
        self._emu.inputs[index].name = new_name
        return None

class GetInputTempCommand:
    def __init__(self, emulator):
        self.id = "KRDG?"
        self._emu = emulator

    def execute_and_reply(self, data):
        return str(self._emu.get_target_input(data).get_temperature())

class GetInputVoltageCommand:
    def __init__(self, emulator):
        self.id = "SRDG?"
        self._emu = emulator

    def execute_and_reply(self, data):
        return str(self._emu.get_target_input(data).raw_voltage)

class GetAlarmStatusCommand:
    def __init__(self, emulator):
        self.id = "ALARMST?"
        self._emu = emulator

    def execute_and_reply(self, data):
        input = self._emu.get_target_input(data)
        return "%d,%d" % (self._emu.bool_to_int(input.has_high_alarm), self._emu.bool_to_int(input.has_low_alarm))

class GetAlarmSettingsCommand:
    def __init__(self, emulator):
        self.id = "ALARM?"
        self._emu = emulator

    def execute_and_reply(self, data):
        input = self._emu.get_target_input(data)
        return "%d,%f,%f,%f,%d,%d,%d" % (input.alarm_enabled, input.alarm_high_setpoint, input.alarm_low_setpoint, \
                                         input.alarm_deadband, input.alarm_latching, input.alarm_audible, \
                                         input.alarm_visible)

class GetReadingStatusCommand:
    def __init__(self, emulator):
        self.id = "RDGST?"
        self._emu = emulator

    def execute_and_reply(self, data):
        return str(self._emu.get_target_input(data).reading_status)

class GetInputCurveNumberCommand:
    def __init__(self, emulator):
        self.id = "INCRV?"
        self._emu = emulator

    def execute_and_reply(self, data):
        return str(self._emu.get_target_input(data).curve_number)

class GetCurveHeaderCommand:
    def __init__(self, emulator):
        self.id = "CRVHDR?"
        self._emu = emulator

    def execute_and_reply(self, data):
        curve = self._emu.get_target_curve(data)
        return "%s,%s,%d,%f,%d" % (curve.name, curve.serial, curve.format, curve.limit, curve.coeff)

class GetInputTypeCommand:
    def __init__(self, emulator):
        self.id = "INTYPE?"
        self._emu = emulator

    def execute_and_reply(self, data):
        input = self._emu.get_target_input(data)
        return "%d,%d,%d,%d,%d" % (input.sensor_type, self._emu.bool_to_int(input.autorange_on), input.range, \
                                   self._emu.bool_to_int(input.compensation_on), input.units)


class Lakeshore336Emulator:
    def __init__(self):#
        self.id = "EmulatedDevice"
        self._populate_inputs()
        self._populate_curves()
        self._populate_outputs()
        self._populate_commands()

    def _populate_inputs(self):
        self.inputs = dict()
        self.inputs["A"] = LakeshoreInput()
        self.inputs["B"] = LakeshoreInput()
        self.inputs["C"] = LakeshoreInput()
        self.inputs["D"] = LakeshoreInput()

    def _populate_outputs(self):
        self.outputs = dict()
        self.outputs["1"] = LakeshoreOutput()
        self.outputs["2"] = LakeshoreOutput()

    def _populate_curves(self):
        self.curves = dict()
        self.curves["15"] = CalibrationCurve()

    def _populate_commands(self):
        self.commands = list()
        self.commands.append(GetIdCommand(self))
        self.commands.append(GetInputNameCommand(self))
        self.commands.append(SetInputNameCommand(self))
        self.commands.append(GetInputTempCommand(self))
        self.commands.append(GetInputVoltageCommand(self))
        self.commands.append(GetAlarmStatusCommand(self))
        self.commands.append(GetAlarmSettingsCommand(self))
        self.commands.append(GetReadingStatusCommand(self))
        self.commands.append(GetInputCurveNumberCommand(self))
        self.commands.append(GetCurveHeaderCommand(self))
        self.commands.append(GetInputTypeCommand(self))

    def process(self, data):
        msg = self._reply(data)
        if msg is not None:
            return msg + "\r\n"

        return None

    def _reply(self, data):
        command_id = data.split()[0]
        (command,) = [cmd for cmd in self.commands if cmd.id == command_id]
        return command.execute_and_reply(data)

#    def _reply(self, data):
#        if data.startswith("SETP?"):
#            return str(self._get_target_output(data).temp_setpoint)
#
#        if data.startswith("SETP "):
#            self._set_setpoint(data)
#            return None
#
#        if data.startswith("RAMP?")
#
#        return None
#
    def bool_to_int(self, bool):
        return 1 if bool else 0

    def get_target_input(self, data):
        index = data[-1]
        return self.inputs[index]

    def get_target_curve(self, data):
        index = data.split()[-1]
        return self.curves[index]
#
#    def _get_target_output(self, data):
#        index = data[-1]
#        return self.outputs[index]
#
    def get_set_tokens(self, data, command):
        return data[len(command + " "):].split(",")
#
#
#    def _set_setpoint(self, data):
#        tokens = self._get_set_tokens(data, "SETP")
#        index = tokens[0]
#        new_temp = float(tokens[1])
#        self.outputs[index].temp_setpoint = new_temp


if __name__ == "__main__":
    port_file = __file__
    dev = Lakeshore336Emulator()
    TelnetEngine().start(dev, port_file)




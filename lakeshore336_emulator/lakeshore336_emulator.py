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
        self.heater_range = 2
        self.manual_output = 20.0
        self.pid = (1.0, 2.0, 3.0)
        self.output_mode = 1
        self.control_input = 1
        self.powerup_enabled = True
        self.heater_output = 21.0
        self.heater_status = 2


class CalibrationCurve:
    def __init__(self):
        self.name = "Emulator curve " # Must be 15 chars
        self.serial = "0123456789" # Must be 10 chars
        self.format = 1
        self.limit = 1000.0
        self.coeff = 2

class NullCommand:
    def execute_and_reply(self, data):
        return None

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

class GetSetpointCommand:
    def __init__(self, emulator):
        self.id = "SETP?"
        self._emu = emulator

    def execute_and_reply(self, data):
        return str(self._emu.get_target_output(data).temp_setpoint)

class SetSetpointCommand:
    def __init__(self, emulator):
        self.id = "SETP"
        self._emu = emulator

    def execute_and_reply(self, data):
        tokens = self._emu.get_set_tokens(data, self.id)
        index = tokens[0]
        new_temp = float(tokens[1])
        self._emu.outputs[index].temp_setpoint = new_temp
        return None

class GetOutputRampCommand:
    def __init__(self, emulator):
        self.id = "RAMP?"
        self._emu = emulator

    def execute_and_reply(self, data):
        output = self._emu.get_target_output(data)
        return "%d,%f" % (output.ramp_on, output.ramp_rate)

class SetOutputRampCommand:
    def __init__(self, emulator):
        self.id = "RAMP"
        self._emu = emulator

    def execute_and_reply(self, data):
        tokens = self._emu.get_set_tokens(data, self.id)
        index = tokens[0]
        ramp_on = self._emu.int_to_bool(int(tokens[1]))
        ramp_rate = float(tokens[2])
        self._emu.outputs[index].ramp_on = ramp_on
        self._emu.outputs[index].ramp_rate = ramp_rate
        return None

class GetHeaterRangeCommand:
    def __init__(self, emulator):
        self.id = "RANGE?"
        self._emu = emulator

    def execute_and_reply(self, data):
        return str(self._emu.get_target_output(data).heater_range)

class SetHeaterRangeCommand:
    def __init__(self, emulator):
        self.id = "RANGE"
        self._emu = emulator

    def execute_and_reply(self, data):
        tokens = self._emu.get_set_tokens(data, self.id)
        index = tokens[0]
        range = int(tokens[1])
        self._emu.outputs[index].heater_range = range
        return None

class GetManualOutputCommand:
    def __init__(self, emulator):
        self.id = "MOUT?"
        self._emu = emulator

    def execute_and_reply(self, data):
        return str(self._emu.get_target_output(data).manual_output)

class SetManualOutputCommand:
    def __init__(self, emulator):
        self.id = "MOUT"
        self._emu = emulator

    def execute_and_reply(self, data):
        tokens = self._emu.get_set_tokens(data, self.id)
        index = tokens[0]
        output = float(tokens[1])
        self._emu.outputs[index].manual_output = output
        return None

class GetPIDCommand:
    def __init__(self, emulator):
        self.id = "PID?"
        self._emu = emulator

    def execute_and_reply(self, data):
        return "%f,%f,%f" % self._emu.get_target_output(data).pid

class SetPIDCommand:
    def __init__(self, emulator):
        self.id = "PID"
        self._emu = emulator

    def execute_and_reply(self, data):
        tokens = self._emu.get_set_tokens(data, self.id)
        index = tokens[0]
        self._emu.outputs[index].pid = tuple([float(t) for t in tokens[1:]])
        return None

class GetOutputModeCommand:
    def __init__(self, emulator):
        self.id = "OUTMODE?"
        self._emu = emulator

    def execute_and_reply(self, data):
        output = self._emu.get_target_output(data)
        return "%d,%d,%d" % (output.output_mode, output.control_input, self._emu.bool_to_int(output.powerup_enabled))

class SetOutputModeCommand:
    def __init__(self, emulator):
        self.id = "OUTMODE"
        self._emu = emulator

    def execute_and_reply(self, data):
        tokens = self._emu.get_set_tokens(data, self.id)
        index = tokens[0]
        output = self._emu.get_target_output(index)
        (mode, ctr_input, powerup) = [int(t) for t in tokens[1:]]
        output.output_mode = mode
        output.control_input = ctr_input
        output.powerup_enabled = self._emu.int_to_bool(powerup)
        return None

class GetHeaterOutputCommand:
    def __init__(self, emulator):
        self.id = "HTR?"
        self._emu = emulator

    def execute_and_reply(self, data):
        return str(self._emu.get_target_output(data).heater_output)

class GetHeaterStatusCommand:
    def __init__(self, emulator):
        self.id = "HTRST?"
        self._emu = emulator

    def execute_and_reply(self, data):
        return str(self._emu.get_target_output(data).heater_status)

class StartAutotuneCommand(NullCommand):
    def __init__(self, emulator):
        self.id = "ATUNE"


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
        self.commands.append(GetSetpointCommand(self))
        self.commands.append(SetSetpointCommand(self))
        self.commands.append(GetOutputRampCommand(self))
        self.commands.append(SetOutputRampCommand(self))
        self.commands.append(GetHeaterRangeCommand(self))
        self.commands.append(SetHeaterRangeCommand(self))
        self.commands.append(GetManualOutputCommand(self))
        self.commands.append(SetManualOutputCommand(self))
        self.commands.append(GetPIDCommand(self))
        self.commands.append(SetPIDCommand(self))
        self.commands.append(GetOutputModeCommand(self))
        self.commands.append(SetOutputModeCommand(self))
        self.commands.append(GetHeaterOutputCommand(self))
        self.commands.append(GetHeaterStatusCommand(self))
        self.commands.append(StartAutotuneCommand(self))

    def process(self, data):
        msg = self._reply(data)
        if msg is not None:
            return msg + "\r\n"

        return None

    def _reply(self, data):
        command_id = data.split()[0]
        try:
            (command,) = [cmd for cmd in self.commands if cmd.id == command_id]
            return command.execute_and_reply(data)
        except ValueError:
            print "***\n*** Command \"%s\" not supported! ***\n***" % (data)
            return None

    def bool_to_int(self, bool):
        return 1 if bool else 0

    def int_to_bool(self, value):
        return value == 1

    def get_target_input(self, data):
        index = data[-1]
        return self.inputs[index]

    def get_target_curve(self, data):
        index = data.split()[-1]
        return self.curves[index]

    def get_target_output(self, data):
        index = data[-1]
        return self.outputs[index]

    def get_set_tokens(self, data, command):
        return data[len(command + " "):].split(",")


if __name__ == "__main__":
    port_file = __file__
    dev = Lakeshore336Emulator()
    TelnetEngine().start(dev, port_file)




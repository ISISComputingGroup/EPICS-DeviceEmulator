import sys, random
sys.path.append("../test_framework")

from telnet_engine import TelnetEngine

class LakeshoreInput(object):
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


class LakeshoreOutput(object):
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


class CalibrationCurve(object):
    def __init__(self):
        self.name = "Emulator curve " # Must be 15 chars
        self.serial = "0123456789" # Must be 10 chars
        self.format = 1
        self.limit = 1000.0
        self.coeff = 2

class LakeshoreModel(object):
    def __init__(self):
        self.id = "EmulatedDevice"
        self._populate_inputs()
        self._populate_curves()
        self._populate_outputs()

    def _populate_inputs(self):
        self._inputs = dict()
        self._inputs["A"] = LakeshoreInput()
        self._inputs["B"] = LakeshoreInput()
        self._inputs["C"] = LakeshoreInput()
        self._inputs["D"] = LakeshoreInput()

    def _populate_outputs(self):
        self._outputs = dict()
        self._outputs["1"] = LakeshoreOutput()
        self._outputs["2"] = LakeshoreOutput()

    def _populate_curves(self):
        self._curves = dict()
        self._curves["15"] = CalibrationCurve()

    def get_input(self, input_key):
        return self._inputs[input_key]

    def get_output(self, output_key):
        return self._outputs[output_key]

    def get_curve(self, curve_key):
        return self._curves[curve_key]


class Command(object):
    def __init__(self, model, id):
        self._model = model
        self.id = id

    def execute_and_reply(self, data):
        return None

    def _get_target_input(self, data):
        index = data[-1]
        return self._model.get_input(index)

    def _get_target_output(self, data):
        index = data[-1]
        return self._model.get_output(index)

    def _get_target_curve(self, data):
        index = data.split()[-1]
        return self._model.get_curve(index)

    def _get_set_tokens(self, data):
        return data[len(self.id + " "):].split(",")

    def _bool_to_int(self, bool):
        return 1 if bool else 0

    def _int_to_bool(self, value):
        return value == 1


class GetIdCommand(Command):
    def __init__(self, model):
        super(GetIdCommand, self).__init__(model, "*IDN?")

    def execute_and_reply(self, data):
        return "LSCI,%s" % (self._model.id)

class GetInputNameCommand(Command):
    def __init__(self, model):
        super(GetInputNameCommand, self).__init__(model, "INNAME?")

    def execute_and_reply(self, data):
        return self._get_target_input(data).name

class SetInputNameCommand(Command):
    def __init__(self, model):
        super(SetInputNameCommand, self).__init__(model, "INNAME")

    def execute_and_reply(self, data):
        tokens = self._get_set_tokens(data)
        index = tokens[0]
        new_name = tokens[1].strip("\"")
        self._model.get_input(index).name = new_name
        return None

class GetInputTempCommand(Command):
    def __init__(self, model):
        super(GetInputTempCommand, self).__init__(model, "KRDG?")

    def execute_and_reply(self, data):
        return str(self._get_target_input(data).get_temperature())

class GetInputVoltageCommand(Command):
    def __init__(self, model):
        super(GetInputVoltageCommand, self).__init__(model, "SRDG?")

    def execute_and_reply(self, data):
        return str(self._get_target_input(data).raw_voltage)

class GetAlarmStatusCommand(Command):
    def __init__(self, model):
        super(GetAlarmStatusCommand, self).__init__(model, "ALARMST?")

    def execute_and_reply(self, data):
        input = self._get_target_input(data)
        return "%d,%d" % (self._bool_to_int(input.has_high_alarm), self._bool_to_int(input.has_low_alarm))

class GetAlarmSettingsCommand(Command):
    def __init__(self, model):
        super(GetAlarmSettingsCommand, self).__init__(model, "ALARM?")

    def execute_and_reply(self, data):
        input = self._get_target_input(data)
        return "%d,%f,%f,%f,%d,%d,%d" % (input.alarm_enabled, input.alarm_high_setpoint, input.alarm_low_setpoint, \
                                         input.alarm_deadband, input.alarm_latching, input.alarm_audible, \
                                         input.alarm_visible)

class GetReadingStatusCommand(Command):
    def __init__(self, model):
        super(GetReadingStatusCommand, self).__init__(model, "RDGST?")

    def execute_and_reply(self, data):
        return str(self._get_target_input(data).reading_status)

class GetInputCurveNumberCommand(Command):
    def __init__(self, model):
        super(GetInputCurveNumberCommand, self).__init__(model, "INCRV?")

    def execute_and_reply(self, data):
        return str(self._get_target_input(data).curve_number)

class GetCurveHeaderCommand(Command):
    def __init__(self, model):
        super(GetCurveHeaderCommand, self).__init__(model, "CRVHDR?")

    def execute_and_reply(self, data):
        curve = self._get_target_curve(data)
        return "%s,%s,%d,%f,%d" % (curve.name, curve.serial, curve.format, curve.limit, curve.coeff)

class GetInputTypeCommand(Command):
    def __init__(self, model):
        super(GetInputTypeCommand, self).__init__(model, "INTYPE?")

    def execute_and_reply(self, data):
        input = self._get_target_input(data)
        return "%d,%d,%d,%d,%d" % (input.sensor_type, self._bool_to_int(input.autorange_on), input.range, \
                                   self._bool_to_int(input.compensation_on), input.units)

class GetSetpointCommand(Command):
    def __init__(self, model):
        super(GetSetpointCommand, self).__init__(model, "SETP?")

    def execute_and_reply(self, data):
        return str(self._get_target_output(data).temp_setpoint)

class SetSetpointCommand(Command):
    def __init__(self, model):
        super(SetSetpointCommand, self).__init__(model, "SETP")

    def execute_and_reply(self, data):
        tokens = self._get_set_tokens(data)
        index = tokens[0]
        new_temp = float(tokens[1])
        self._model.get_output(index).temp_setpoint = new_temp
        return None

class GetOutputRampCommand(Command):
    def __init__(self, model):
        super(GetOutputRampCommand, self).__init__(model, "RAMP?")

    def execute_and_reply(self, data):
        output = self._get_target_output(data)
        return "%d,%f" % (output.ramp_on, output.ramp_rate)

class SetOutputRampCommand(Command):
    def __init__(self, model):
        super(SetOutputRampCommand, self).__init__(model, "RAMP")

    def execute_and_reply(self, data):
        tokens = self._get_set_tokens(data)
        index = tokens[0]
        ramp_on = self._int_to_bool(int(tokens[1]))
        ramp_rate = float(tokens[2])
        self._model.get_output(index).ramp_on = ramp_on
        self._model.get_output(index).ramp_rate = ramp_rate
        return None

class GetHeaterRangeCommand(Command):
    def __init__(self, model):
        super(GetHeaterRangeCommand, self).__init__(model, "RANGE?")

    def execute_and_reply(self, data):
        return str(self._get_target_output(data).heater_range)

class SetHeaterRangeCommand(Command):
    def __init__(self, model):
        super(SetHeaterRangeCommand, self).__init__(model, "RANGE")

    def execute_and_reply(self, data):
        tokens = self._get_set_tokens(data)
        index = tokens[0]
        range = int(tokens[1])
        self._model.get_output(index).heater_range = range
        return None

class GetManualOutputCommand(Command):
    def __init__(self, model):
        super(GetManualOutputCommand, self).__init__(model, "MOUT?")

    def execute_and_reply(self, data):
        return str(self._get_target_output(data).manual_output)

class SetManualOutputCommand(Command):
    def __init__(self, model):
        super(SetManualOutputCommand, self).__init__(model, "MOUT")

    def execute_and_reply(self, data):
        tokens = self._get_set_tokens(data)
        index = tokens[0]
        man_output = float(tokens[1])
        self._model.get_output(index).manual_output = man_output
        return None

class GetPIDCommand(Command):
    def __init__(self, model):
        super(GetPIDCommand, self).__init__(model, "PID?")

    def execute_and_reply(self, data):
        return "%f,%f,%f" % self._get_target_output(data).pid

class SetPIDCommand(Command):
    def __init__(self, model):
        super(SetPIDCommand, self).__init__(model, "PID")

    def execute_and_reply(self, data):
        tokens = self._get_set_tokens(data)
        index = tokens[0]
        self._model.get_output(index).pid = tuple([float(t) for t in tokens[1:]])
        return None

class GetOutputModeCommand(Command):
    def __init__(self, model):
        super(GetOutputModeCommand, self).__init__(model, "OUTMODE?")

    def execute_and_reply(self, data):
        output = self._get_target_output(data)
        return "%d,%d,%d" % (output.output_mode, output.control_input, self._bool_to_int(output.powerup_enabled))

class SetOutputModeCommand(Command):
    def __init__(self, model):
        super(SetOutputModeCommand, self).__init__(model, "OUTMODE")

    def execute_and_reply(self, data):
        tokens = self._get_set_tokens(data)
        index = tokens[0]
        output = self._get_target_output(index)
        (mode, ctr_input, powerup) = [int(t) for t in tokens[1:]]
        output.output_mode = mode
        output.control_input = ctr_input
        output.powerup_enabled = self._int_to_bool(powerup)
        return None

class GetHeaterOutputCommand(Command):
    def __init__(self, model):
        super(GetHeaterOutputCommand, self).__init__(model, "HTR?")

    def execute_and_reply(self, data):
        return str(self._get_target_output(data).heater_output)

class GetHeaterStatusCommand(Command):
    def __init__(self, model):
        super(GetHeaterStatusCommand, self).__init__(model, "HTRST?")

    def execute_and_reply(self, data):
        return str(self._get_target_output(data).heater_status)

class StartAutotuneCommand(Command):
    def __init__(self, model):
        super(StartAutotuneCommand, self).__init__(model, "ATUNE")


class Lakeshore336Emulator(object):
    def __init__(self):
        self._model = LakeshoreModel()
        self._populate_commands()

    def _populate_commands(self):
        self.commands = list()
        self.commands.append(GetIdCommand(self._model))
        self.commands.append(GetInputNameCommand(self._model))
        self.commands.append(SetInputNameCommand(self._model))
        self.commands.append(GetInputTempCommand(self._model))
        self.commands.append(GetInputVoltageCommand(self._model))
        self.commands.append(GetAlarmStatusCommand(self._model))
        self.commands.append(GetAlarmSettingsCommand(self._model))
        self.commands.append(GetReadingStatusCommand(self._model))
        self.commands.append(GetInputCurveNumberCommand(self._model))
        self.commands.append(GetCurveHeaderCommand(self._model))
        self.commands.append(GetInputTypeCommand(self._model))
        self.commands.append(GetSetpointCommand(self._model))
        self.commands.append(SetSetpointCommand(self._model))
        self.commands.append(GetOutputRampCommand(self._model))
        self.commands.append(SetOutputRampCommand(self._model))
        self.commands.append(GetHeaterRangeCommand(self._model))
        self.commands.append(SetHeaterRangeCommand(self._model))
        self.commands.append(GetManualOutputCommand(self._model))
        self.commands.append(SetManualOutputCommand(self._model))
        self.commands.append(GetPIDCommand(self._model))
        self.commands.append(SetPIDCommand(self._model))
        self.commands.append(GetOutputModeCommand(self._model))
        self.commands.append(SetOutputModeCommand(self._model))
        self.commands.append(GetHeaterOutputCommand(self._model))
        self.commands.append(GetHeaterStatusCommand(self._model))
        self.commands.append(StartAutotuneCommand(self._model))

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


if __name__ == "__main__":
    port_file = __file__
    dev = Lakeshore336Emulator()
    TelnetEngine().start(dev, port_file)




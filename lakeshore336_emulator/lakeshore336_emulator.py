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


class CalibrationCurve:
    def __init__(self):
        self.name = "Emulator curve " # Must be 15 chars
        self.serial = "0123456789" # Must be 10 chars
        self.format = 1
        self.limit = 1000.0
        self.coeff = 2


class Lakeshore336Emulator:
    def __init__(self):
        self.id = "EmulatedDevice"

        self.inputs = dict()
        self.inputs["A"] = LakeshoreInput()
        self.inputs["B"] = LakeshoreInput()
        self.inputs["C"] = LakeshoreInput()
        self.inputs["D"] = LakeshoreInput()

        self.curves = dict()
        self.curves["15"] = CalibrationCurve()

    def process(self, data):
        msg = self._reply(data)
        if msg is not None:
            return msg + "\r\n"

        return None

    def _reply(self, data):
        if data == "*IDN?":
            return "LSCI,%s" % (self.id)

        if data.startswith("INNAME?"):
            return self._get_target_input(data).name

        if data.startswith("INNAME"):
            self._set_input_name(data)
            return None

        if data.startswith("KRDG?"):
            return str(self._get_target_input(data).get_temperature())

        if data.startswith("SRDG?"):
            return str(self._get_target_input(data).raw_voltage)

        if data.startswith("ALARMST?"):
            return self._get_alarm_status(data)

        if data.startswith("ALARM?"):
            return self._get_alarm_settings(data)

        if data.startswith("RDGST?"):
            return str(self._get_target_input(data).reading_status)

        if data.startswith("INCRV?"):
            index = data[-1]
            return str(self.inputs[index].curve_number)

        if data.startswith("CRVHDR?"):
            return self._get_curve_header(data)

        if data.startswith("INTYPE?"):
            return self._get_input_type(data)

        return None

    def _bool_to_int(self, bool):
        return 1 if bool else 0

    def _get_target_input(self, data):
        index = data[-1]
        return self.inputs[index]

    def _get_target_curve(self, data):
        index = data.split()[-1]
        return self.curves[index]

    def _set_input_name(self, data):
        tokens = data[len("INNAME "):].split(",")
        index = tokens[0]
        new_name = tokens[1].strip("\"")
        self.inputs[index].name = new_name

    def _get_alarm_status(self, data):
        input = self._get_target_input(data)
        return "%d,%d" % (self._bool_to_int(input.has_high_alarm), self._bool_to_int(input.has_low_alarm))

    def _get_alarm_settings(self, data):
        input = self._get_target_input(data)
        return "%d,%f,%f,%f,%d,%d,%d" % (input.alarm_enabled, input.alarm_high_setpoint, input.alarm_low_setpoint, \
                                         input.alarm_deadband, input.alarm_latching, input.alarm_audible, \
                                         input.alarm_visible)

    def _get_curve_header(self, data):
        curve = self._get_target_curve(data)
        return "%s,%s,%d,%f,%d" % (curve.name, curve.serial, curve.format, curve.limit, curve.coeff)

    def _get_input_type(self, data):
        input = self._get_target_input(data)
        return "%d,%d,%d,%d,%d" % (input.sensor_type, self._bool_to_int(input.autorange_on), input.range, \
                                   self._bool_to_int(input.compensation_on), input.units)

if __name__ == "__main__":
    port_file = __file__
    dev = Lakeshore336Emulator()
    TelnetEngine().start(dev, port_file)




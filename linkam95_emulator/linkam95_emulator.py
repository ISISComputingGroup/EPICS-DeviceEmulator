import sys, random
sys.path.append("../test_framework")

from telnet_engine import TelnetEngine

PUMP_MODE_AUTO = "AUTO"
PUMP_MODE_MANUAL = "MANUAL"

T95_STATE_STOP = "stopped"
T95_STATE_HEAT = "heat"
T95_STATE_COOL = "cool"
T95_STATE_HOLD = "hold"

class LinkamModel(object):
    def __init__(self):
        self.id = "EmulatedDevice"
        self.ramp_state = T95_STATE_STOP
        self.temperature_sp = 0.0
        self.ramp_rate = 1.0
        self.pump_mode = PUMP_MODE_AUTO
        self.temperature = 0.0
        self.pump_speed = 0
        self.command_hold = False
        
    def get_status_bytes(self):
        Tarray = [0x80] * 10

        # Status byte (SB1)
        Tarray[0] = {
            T95_STATE_STOP: 0x01,
            T95_STATE_HEAT: 0x10,
            T95_STATE_COOL: 0x20,
            T95_STATE_HOLD: 0x30,
        }.get(self.ramp_state, 0x01)
        if Tarray[0] == 0x30 and self.command_hold:
            Tarray[0] =  0x50

        # Pump status byte (PB1)
        Tarray[2] = 0x80 + self.pump_speed

        # Temperature
        self._update_temperature()
        Tarray[6:10] = [ord(x) for x in "%04x" % (int(self.temperature * 10) & 0xFFFF)]

        return ''.join(chr(c) for c in Tarray)
        
    def start(self):
        if self.ramp_state == T95_STATE_STOP:
            self.ramp_state = T95_STATE_HOLD
            self._update_state()
    
    def stop(self):
        self.ramp_state = T95_STATE_STOP
    
    def heat(self):
        self.unhold()
    
    def cool(self):
        self.unhold()
    
    def hold(self):
        self.command_hold = True
        self._update_state()
        
    def unhold(self):
        self.command_hold = False
        self._update_state()
    
    def _update_state(self):
        if self.ramp_state == T95_STATE_STOP:
            return
        elif self.command_hold:
            self.ramp_state = T95_STATE_HOLD
        elif self.temperature_sp < self.temperature:
            self.ramp_state = T95_STATE_COOL
        elif self.temperature_sp > self.temperature:
            self.ramp_state = T95_STATE_HEAT
        else:
            self.ramp_state = T95_STATE_HOLD
            
    def _update_temperature(self):
        import math
        if self.ramp_state!=T95_STATE_HOLD and self.ramp_state!=T95_STATE_STOP:
            self.temperature += math.copysign(1, self.temperature_sp-self.temperature)*self.ramp_rate/60.0
            if self.ramp_state == T95_STATE_COOL:
                self.pump_speed = min(int(self.ramp_rate/3),30)
            else:
                self.pump_speed = 0
        self._update_state()

class Command(object):
    def __init__(self, model, id):
        self._model = model
        self.id = id

    def execute_and_reply(self, data):
        return None

    def _get_set_token(self, data):
        return data[2:]


class GetStatusCommand(Command):
    def __init__(self, model):
        super(GetStatusCommand, self).__init__(model, "T")

    def execute_and_reply(self, data):
        return self._model.get_status_bytes()

class SetRateCommand(Command):
    def __init__(self, model):
        super(SetRateCommand, self).__init__(model, "R")

    def execute_and_reply(self, data):
        self._model.ramp_rate = int(self._get_set_token(data))/100.0
        return None

class SetLimitCommand(Command):
    def __init__(self, model):
        super(SetLimitCommand, self).__init__(model, "L")

    def execute_and_reply(self, data):
        self._model.temperature_sp = float(self._get_set_token(data))/10.0
        return None

class StartRampControlCommand(Command):
    def __init__(self, model):
        super(StartRampControlCommand, self).__init__(model, "S")

    def execute_and_reply(self, data):
        self._model.start()
        return None

class StopRampControlCommand(Command):
    def __init__(self, model):
        super(StopRampControlCommand, self).__init__(model, "E")

    def execute_and_reply(self, data):
        self._model.stop()
        return None

class ForceHeatControlCommand(Command):
    def __init__(self, model):
        super(ForceHeatControlCommand, self).__init__(model, "H")

    def execute_and_reply(self, data):
        self._model.heat()
        return None

class ForceCoolControlCommand(Command):
    def __init__(self, model):
        super(ForceCoolControlCommand, self).__init__(model, "C")

    def execute_and_reply(self, data):
        self._model.cool()
        return None

class HoldControlCommand(Command):
    def __init__(self, model):
        super(HoldControlCommand, self).__init__(model, "O")

    def execute_and_reply(self, data):
        self._model.hold()
        return None

class SetPumpStateCommand(Command):
    def __init__(self, model):
        super(SetPumpStateCommand, self).__init__(model, "P")

    def execute_and_reply(self, data):
        token = self._get_set_token(data)
        if token == "a":
            self._model.pump_mode = PUMP_MODE_AUTO
        elif token == "m":
            self._model.pump_mode = PUMP_MODE_MANUAL
        else:
            try:
                speed = ord(token)
                if token in range(0,31):
                    self._model.pump_speed = token
            except:
                pass
        return None

class Linkam95Emulator(object):
    def __init__(self):
        self._model = LinkamModel()
        self._populate_commands()

    def _populate_commands(self):
        self.commands = list()
        self.commands.append(SetPumpStateCommand(self._model))
        self.commands.append(HoldControlCommand(self._model))
        self.commands.append(ForceCoolControlCommand(self._model))
        self.commands.append(ForceHeatControlCommand(self._model))
        self.commands.append(StopRampControlCommand(self._model))
        self.commands.append(StartRampControlCommand(self._model))
        self.commands.append(SetLimitCommand(self._model))
        self.commands.append(SetRateCommand(self._model))
        self.commands.append(GetStatusCommand(self._model))

    def process(self, data):
        msg = self._reply(data)
        if msg is None:
            msg = ""
        return msg + "\r"

        return None

    def _reply(self, data):
        command_id = data[0]
        try:
            (command,) = [cmd for cmd in self.commands if cmd.id == command_id]
            return command.execute_and_reply(data)
        except ValueError:
            print "***\n*** Command \"%s\" not supported! ***\n***" % (data)
            return None


if __name__ == "__main__":
    port_file = __file__
    dev = Linkam95Emulator()
    TelnetEngine().start(dev, port_file)




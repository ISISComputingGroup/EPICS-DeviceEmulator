from lewis.adapters.stream import StreamInterface, Cmd
from threading import Timer

START_COMM = "START01"
BEAMON_COMM = "BEAMON"
BEAMOFF_COMM = "BEAMOFF"

class GamryStreamInterface(StreamInterface):

    commands = {
        Cmd("start_charging", "^" + START_COMM + "$"),
        Cmd("beam_on", "^" + BEAMON_COMM + "$"),
        Cmd("beam_off", "^" + BEAMOFF_COMM + "$"),
    }

    in_terminator = "\r"
    out_terminator = "\r"
    charging_time = 10.0

    def beam_on(self):
        return "BEAMON"

    def beam_off(self):
        return "BEAMOFF"

    def charged(self):
        self.handler.unsolicitedReply("STOPPED")

    def start_charging(self):
        t = Timer(self.charging_time, self.charged)
        t.start()
        return "STARTED"

    def handle_error(self, request, error):
        print "An error occurred at request " + repr(request) + ": " + repr(error)
        return "NAC"

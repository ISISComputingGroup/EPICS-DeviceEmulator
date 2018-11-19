from lewis.adapters.stream import StreamInterface

from lewis.core.logging import has_log
from lewis_emulators.utils.replies import conditional_reply
from lewis_emulators.utils.command_builder import CmdBuilder

if_connected = conditional_reply('connected')

@has_log
class Knr1050StreamInterface(StreamInterface):

    in_terminator = '\r'
    out_terminator = '\r'

    def __init__(self):

        super(Knr1050StreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.get_status).escape("STATUS:").int().eos().build(),
            CmdBuilder(self.ramp).escape("RAMP:0,").float().escape(",").float().escape(",").float().escape(",").float().escape(",").float().build(),
            CmdBuilder(self.stop).escape("STOP:1,0").build(),
            CmdBuilder(self.stop_klv).escape("STOP:2").build(),
            CmdBuilder(self.get_pressure_limits).escape("PLIM?").build(),
            CmdBuilder(self.set_pressure_limits).escape("PLIM:").float().escape(",").float().eos().build()
        }


    def handle_error(self, request, error):
        """
        If command is not recognised print and error
        Args:
            request: requested string
            error: problem
        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def ramp(self, flow_rate, A, B, C, D):
        """
        Executes ramp starting from current execution time.
        Args:
            flow_rate (float): the flow rate in ul/min
            A (float): concentration A
            B (float): concentration B
            C (float): concentration C
            D (float): concentration D
        """
        self.device.flow_rate = flow_rate
        self.device.concentration_A = A
        self.device.concentration_B = B
        self.device.concentration_C = C
        self.device.concentration_D = D
        self.device.ramp_status = True


    def stop(self):
        """
        Stop mode: Stop time table and data acquisition.
        """
        self.device.is_stopped = True


    def stop_klv(self):
        """
        Stop mode: Keep last values.
        """
        self.device.keep_last_values = True
        self.device.ramp_status = False

    def get_pressure_limits(self):
        return "PLIM:{},{}".format(self.device.pressure_limit_low, self.device.pressure_limit_high)

    def set_pressure_limits(self, low, high):
        self.device.pressure_limit_low = low
        self.device.pressure_limit_high = high

    def get_status(self, instrument_state):
        self.device.current_instrument_state = instrument_state

from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder

@has_log
class GemorcStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_id").escape("id").build(),
        CmdBuilder("initialise").escape("in").build(),
        CmdBuilder("re_zero_to_datum").escape("da").build(),
        CmdBuilder("start").escape("st").build(),
        CmdBuilder("stop").escape("sp").build(),
        CmdBuilder("stop_next_initialisation").escape("si").build(),
        CmdBuilder("set_window_width").escape("ww").int().build(),
        CmdBuilder("set_offset").escape("of").int().build(),
        CmdBuilder("set_speed").escape("ds").int().build(),
        CmdBuilder("set_acceleration").escape("ac").int().build(),
        CmdBuilder("get_status").escape("rq").build(),
    }

    in_terminator = "\r"
    out_terminator = "\r"

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def get_id(self):
        """
        Returns:
            Device's PnP identity
        """
        return "IBEX GEMORC DEVICE EMULATOR"

    def initialise(self):
        """
        Initialise the collimator after 1 turn rotation
        """
        self.device.initialise()
        return "OK"

    def re_zero_to_datum(self):
        """
        Re-zero position from datum marker
        """
        self.device.re_zero_to_datum()
        return "OK"

    def start(self):
        """
        Start motion
        """
        self.device.start()
        return "OK"

    def stop(self):
        """
        Stop motion
        """
        self.device.stop()
        return "OK"

    def stop_next_initialisation(self):
        """
        Stop motion after next auto-initialisation
        """
        self.device.stop_next_initialisation()
        return "OK"

    def set_window_width(self, width):
        """
        Sets the window width

        Args:
            width: Width in centi-degrees
        """
        self.device.set_window_width(int(width))
        return "OK"

    def set_offset(self, offset):
        """
        Sets the offset position from datum to match axis (signed)

        Args:
            offset: Datum offset in centi-degrees
        """
        self.device.set_offset(int(offset))
        return "OK"

    def set_acceleration(self, acceleration):
        """
        Sets the acceleration rate for reversals

        Args:
            acceleration: Rate of acceleration in centi-degrees per second^2
        """
        self.device.set_acceleration(int(acceleration))
        return "OK"

    def set_speed(self, speed):
        """
        Sets the radial speed

        Args:
            speed: Speed in centi-degrees per second
        """
        self.device.set_speed(int(speed))
        return "OK"

    def get_status(self):
        """
        Get the current state of the collimator. This is backwards engineered from the VI. I haven't actually seen
        what the real thing returns as the VI code doesn't match the spec
        """
        request_format = "{oscillating:01d}    {initialising:01d}    {initialised:01d}     {width:03d}     " \
                         "{offset:+04d}      {speed:02d}     {acceleration:03d}  {cycles:05d}          {backlash:03d}"
        status_string = request_format.format(
            oscillating=int(self.device.is_oscillating()),
            initialising=int(self.device.is_initialising()),
            initialised=int(self.device.has_been_initialised()),
            width=int(self.device.get_window_width()),
            offset=int(self.device.get_offset()),
            speed=int(self.device.get_speed()),
            acceleration=int(self.device.get_acceleration()),
            cycles=int(self.device.get_complete_cycles()),
            backlash=int(self.device.get_backlash())
        )
        return status_string

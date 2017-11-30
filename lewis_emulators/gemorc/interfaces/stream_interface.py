from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder

@has_log
class GemorcStreamInterface(StreamInterface):

    # Commands that we expect via serial during normal operation
    commands = {
        CmdBuilder("get_id").escape("id").build(),
        CmdBuilder("initialise").escape("in").build(),
        CmdBuilder("rezero_to_datum").escape("da").build(),
        CmdBuilder("start").escape("st").build(),
        CmdBuilder("stop").escape("sp").build(),
        CmdBuilder("stop_next_initialisation").escape("si").build(),
        CmdBuilder("set_window_width").escape("ww").int().build(),
        CmdBuilder("set_offset_from_datum").escape("of").int().build(),
        CmdBuilder("set_radial_speed").escape("ds").int().build(),
        CmdBuilder("set_radial_acceleration").escape("ac").int().build(),
        CmdBuilder("get_status").escape("rq"),
    }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))
from .kepco_base import KepcoStreamInterface

from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")

__all__ = ["KepcoNoRemStreamInterface"]


@has_log
class KepcoNoRemStreamInterface(KepcoStreamInterface, StreamInterface):
    """
    A stream interface for the kepco with no remote command available
    """

    protocol = "no_rem"

    @if_connected
    def set_control_mode(self, mode):
        raise ValueError("No SYST:REM command available")


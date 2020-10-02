from .kepco_base import KepcoStreamInterface

from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")

__all__ = ["KepcoRemStreamInterface"]


@has_log
class KepcoRemStreamInterface(KepcoStreamInterface, StreamInterface):
    """
    A stream interface for the kepco with the remote command available.
    """

    protocol = "with_rem"

    @if_connected
    def set_control_mode(self, mode):
        mode = int(mode)
        if mode not in [0, 1]:
            raise ValueError("Invalid mode in set_control_mode: {}".format(mode))
        self._device.remote_comms_enabled = (mode == 1)


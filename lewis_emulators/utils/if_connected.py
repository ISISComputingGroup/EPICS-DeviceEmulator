"""
Decorator for creating disconnected behaviour in a emulator stream interface for a device.

Requires:
    Device class in the emulator has a connected flag.

Example usage:

    @if_connected
    def acknowledge_pressure(channel):
        return ACK

acknowledge_pressure returns None if device is not connected and ACK if so.
"""


def if_connected(f):
    """
    Decorator that executes f if the device is connected and returns None otherwise.

    Args:
        f: function to be executed if the device is connected.

    Returns:
       The value of f(*args) if the device is connected and None otherwise.
   """

    def wrapper(*args):
        connected = getattr(args[0], "_device").connected
        if connected:
            result = f(*args)
        else:
            result = None
        return result
    return wrapper

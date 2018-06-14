import six


def conditional_reply(property_name):
    """
    Decorator that executes the command and replies if the device has a member called 'property name' and it is True in
    a boolean context

    Args:
        property_name: The name of the property to look for on the device

    Returns:
       The function returns as normal if property is true. The command is not executed and there is no reply if
       property is false

    Raises:
        - AttributeError if the first argument of the decorated function (self) does not contain .device or ._device
        - AttributeError if the device does not contain a property called property_name

    Usage:
        @conditional_reply("connected")
        def acknowledge_pressure(channel):
            return ACK
    """
    def decorator(func):
        @six.wraps(func)
        def wrapper(self, *args, **kwargs):

            try:
                device = self.device
            except AttributeError:
                try:
                    device = self._device
                except AttributeError:
                    raise AttributeError("Expected device to be accessible as either self.device or self._device")

            try:
                do_reply = getattr(device, property_name)
                return func(self, *args, **kwargs) if do_reply else None
            except AttributeError:
                raise AttributeError(
                    "Expected device to contain an attribute called '{}' but it wasn't found.".format(property_name))

        return wrapper
    return decorator

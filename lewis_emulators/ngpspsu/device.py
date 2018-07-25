from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from enum import Enum


class Status(Enum):
    Off = 0
    On = 1


class SimulatedNgpspsu(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.__model_no_and_firmware = "NGPS 100-50:0.9.01"
        self.__status = Status.Off

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    @property
    def model_number_and_firmware(self):
        """
        Returns the model number and firmware version.
        """

        return self.__model_no_and_firmware

    @property
    def status(self):
        """
        Returns the status of the device (Off or On).
        """

        return self.__status.name

    def turn_on_device(self):
        """
        Turns on the device.

        Returns:
            string: "#AK" if successful. #NK:%i if not where %i is an error
                code.
        """
        if self.__status == Status.On:
            return "#NAK:09"
        elif self.__status == Status.Off:
            self.__status = Status.On
            return "#AK"
        else:
            return "#NAK99"

    def turn_off_device(self):
        """
        Turns off the device.

        Returns:
            string: "#AK" if successful. #NK:%i otherwise where %i is an error
                code.
        """
        if self.__status == Status.Off:
            return "#NAK:13"
        elif self.__status == Status.On:
            self.__status = Status.Off
            return "#AK"
        else:
            return "#NAK99"

    def get_status_via_the_backdoor(self):
        """
        Gets the status of the device as a string.
        Only called via the backdoor.

        Returns:
            string: name of the status of the device
        """
        return self.__status.name

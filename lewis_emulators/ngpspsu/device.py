from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedNgpspsu(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.__model_no_and_firmware = "NGPS 100-50:0.9.01"
        self.__status = ['0'] * 8

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

        return "".join(self.__status)

    def start_device(self):
        """
        Turns on the device.

        Returns:
            string: "#AK" if successful. #NK:%i if not where %i is an error
                code.
        """
        if self.__status[0] == '1':
            return "#NAK:09"
        elif self.__status[0] == '0':
            self.__status[0] = '1'
            return "#AK"
        else:
            return "#NAK99"

    def stop_device(self):
        """
        Turns off the device.

        Returns:
            string: "#AK" if successful. #NK:%i otherwise where %i is an error
                code.
        """
        if self.__status[0] == '0':
            return "#NAK:13"
        elif self.__status[0] == '1':
            self.__status[0] = '0'
            return "#AK"
        else:
            return "#NAK99"

    def reset_device(self):
        """
        Resets the device.

        Returns:
            string: "#AK" if successful. #NK:%i otherwise where %i is an error
                code.
        """
        self.__status = [['0']*4] * 8
        return "#AK"

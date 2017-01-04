from ethernet_device import EthernetDevice


class HmiDevice(EthernetDevice):

    OK_STATUS = "OK"

    def __init__(self, ip):
        self.status = HmiDevice.OK_STATUS
        self.base_page = 34
        self.sub_page = 2
        self.count_cycles = ["999", "006", "002", "002", "002", "002", "002", "002", "001", "001", "310"]
        super(HmiDevice, self).__init__(ip)

    def base_page_string(self):
        return str(self.base_page).zfill(3)

    def sub_page_string(self):
        return str(self.sub_page).zfill(3)

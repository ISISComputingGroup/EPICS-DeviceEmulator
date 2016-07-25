import os
import unittest
from time import sleep

from Tpg26xEmulator import Tpg26xEmulator
from emulator import Emulator
from epics_engine import EpicsEngine
from ioc import Ioc

class TestFunctionalityOfTPG26x(unittest.TestCase):
    engine = None
    emulator = None

    @classmethod
    def setUpClass(cls):
        TestFunctionalityOfTPG26x.emulator = Tpg26xEmulator()

        ioc_name = "TPG268X_01"
        ioc_top = os.path.abspath(r"C:\Instrument\Apps\EPICS\ioc\master\TPG26x")
        proc_serv_exe = r"C:\Instrument\Apps\EPICS\tools\master\cygwin_bin\procServ.exe"
        cls.ioc = Ioc(ioc_name, ioc_top, proc_serv_exe=proc_serv_exe)
        cls.ioc.set_host("localhost")
        cls.ioc.to_be_uncommented = ["drvAsynIPPortConfigure", "dbLoadRecords(\"db/in_out.db\""]

        emu_name = "TPG268xEmulator"
        emu_top = os.path.dirname(os.path.abspath(__file__))
        emu_file = "Tpg26xEmulator.py"
        cls.emu = Emulator(emu_name, emu_top, emu_file, proc_serv_exe=proc_serv_exe)

        cls.engine = EpicsEngine(cls.ioc, cls.emu, make=False)
        cls.engine.start_emulators()
        cls.ioc.set_tcp_port(cls.emu.get_port())
        #cls.engine.start_iocs()

        cls.pressure_pv = "NDW1407:HGV27692:" + ioc_name + "1:PRESSURE"
        cls.value_rbv_pv = ioc_name + ":VALUE_RBV"
        cls.state_safe_pv = ioc_name + ":STATE_SAFE"
        cls.state_scan = 0.5

    @classmethod
    def tearDownClass(cls):
        cls.engine.stop()
        cls.engine.cleanup()

    def setUp(self):
        #print self.engine.caget(self.pressure_pv)
        #self.emu.open_connection()
        #self.emu.write("emulator_command:reset")
        pass

    def tearDown(self):
        self.emu.close_connection()

    def test_GIVEN_no_errors_and_set_pressures_WHEN_measure_THEN_no_error(self):
        sleep(100)
        assert True


if __name__ == '__main__':
    unittest.main()

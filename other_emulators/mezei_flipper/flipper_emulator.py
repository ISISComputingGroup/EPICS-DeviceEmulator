import sys
import types
from mock import MagicMock
import argparse


class _FakeQtCore(object):
    @classmethod
    def pyqtSignal(cls, *a, **k):
        return None

fake_qt_module = types.ModuleType("PyQt5")
fake_qt_module.QtWidgets = MagicMock()
fake_qt_module.QtCore = _FakeQtCore
fake_qt_module.QtNetwork = MagicMock()
sys.modules["PyQt5"] = fake_qt_module

fake_qplot_module = types.ModuleType("QPlot")
fake_qplot_module.QPlot = MagicMock()
sys.modules["QPlot"] = fake_qplot_module

sys.modules["DAQTasks_2flippers"] = MagicMock()

fake_flippr_module = types.ModuleType("flippr_3")
fake_flippr_module.Ui_Flippr = MagicMock()
sys.modules["flippr_3"] = fake_flippr_module


class _UpdatedValue(object):
    """
    This class fake-implements the interface of a pyqtsignal.
    """
    def __init__(self, init_val):
        self._val = init_val

    def value(self):
        return self._val

    def emit(self, value):
        self._val = value


class _Parent(object):
    def __init__(self):
        self.comp_spin_P = _UpdatedValue(0)
        self.comp_spin_A = _UpdatedValue(0)
        self.amplitude_spin_P = _UpdatedValue(0)
        self.amplitude_spin_A = _UpdatedValue(0)
        self.decay_spin_P = _UpdatedValue(0)
        self.decay_spin_A = _UpdatedValue(0)
        self.DeltaT_P = _UpdatedValue(0)
        self.DeltaT_A = _UpdatedValue(0)
        self.filename_P = _UpdatedValue("C:\\file_p.txt")
        self.filename_A = _UpdatedValue("C:\\file_a.txt")
        self.running = _UpdatedValue(True)


from main_andy_2flippers import SignalServer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Test an IOC under emulation by running tests against it')
    parser.add_argument('-p', '--port', type=int, help="The TCP port to run the server on.")
    arguments = parser.parse_args()

    parent = _Parent()

    # We don't know what these objects are under the hood (we don't have that piece of code), so monkey-patch
    # the mapping here.
    SignalServer.toggle = parent.running
    SignalServer.comp_p = parent.comp_spin_P
    SignalServer.comp_a = parent.comp_spin_A
    SignalServer.amp_p = parent.amplitude_spin_P
    SignalServer.amp_a = parent.amplitude_spin_A
    SignalServer.const_p = parent.decay_spin_P
    SignalServer.const_a = parent.decay_spin_A
    SignalServer.dt_a = parent.DeltaT_A
    SignalServer.dt_p = parent.DeltaT_P
    SignalServer.fn_p = parent.filename_P
    SignalServer.fn_a = parent.filename_A

    server = SignalServer("localhost", arguments.port, parent)

    server.listen()
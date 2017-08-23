from lewis.devices import StateMachineDevice
from collections import OrderedDict
from .states import DefaultState

class SimulatedHFMAGPSU(StateMachineDevice):


    def _initialize_data(self):
        self._direction = '-'
        self._outputMode = 'OFF'
        self._rampTarget = 'ZERO'
        self._heaterStatus = 'OFF'   # off or on
        self._heaterValue = 1.0 # V
        self._maxTarget = 5.0
        self._midTarget = 2.5
        self._rampRate = 10.0
        self._pause = 'OFF'
        self._limit = 10
        self._logMessage = "test"
        #self._update = "update field"

    def _get_state_handlers(self):
        return {DefaultState.NAME: DefaultState()}

    def _get_initial_state(self):
        return DefaultState.NAME

    def _get_transition_handlers(self):
        return OrderedDict()

    @property
    def direction(self):
        return self._direction

    @property
    def outputMode(self):
        return self._outputMode

    @property
    def rampTarget(self):
        return self._rampTarget

    @property
    def heaterStatus(self):
        return self._heaterStatus

    @property
    def heaterValue(self):
        return self._heaterValue

    @property
    def maxTarget(self):
        return self._maxTarget

    @property
    def midTarget(self):
        return self._midTarget

    @property
    def rampRate(self):
        return self._rampRate

    @property
    def pause(self):
        return self._pause

    @property
    def limit(self):
        return self._limit

    #@property
    #def update(self):
       # return self._update

    @property
    def logMessage(self):
        return self._logMessage

    @direction.setter
    def direction(self, d):
        self._direction = d

    @outputMode.setter
    def outputMode(self, om):
        self._outputMode = om

    @rampTarget.setter
    def rampTarget(self, rt):
        self._rampTarget = rt

    @heaterStatus.setter
    def heaterStatus(self, hs):
        self._heaterStatus = hs

    @heaterValue.setter
    def heaterValue(self, hv):
        self._heaterValue = hv

    @maxTarget.setter
    def maxTarget(self, mt):
        self._maxTarget = mt

    @midTarget.setter
    def midTarget(self, mt):
        self._midTarget = mt

    @rampRate.setter
    def rampRate(self, rate):
        self._rampRate = rate

    @pause.setter
    def pause(self, p):
        self._pause = p

    @limit.setter
    def limit(self, lim):
        self._limit = lim

    @logMessage.setter
    def logMessage(self, lm):
        self._logMessage = lm

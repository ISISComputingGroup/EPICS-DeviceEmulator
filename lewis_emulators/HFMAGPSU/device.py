from lewis.devices import StateMachineDevice
from collections import OrderedDict
from .states import DefaultState





class SimulatedHFMAGPSU(StateMachineDevice):


    def _initialize_data(self):
        self._isOutputModeTesla = False
        self._isHeaterOn = False
        self._isPaused = False
        self._direction = 0
        self._rampTarget = 0
        self._heaterValue = 1.0
        self._maxTarget = 5.0
        self._midTarget = 2.5
        self._rampRate = 10.0
        self._limit = 10
        self._logMessage = "this is the initial log message"

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
    def isOutputModeTesla(self):
        return self._isOutputModeTesla

    @property
    def rampTarget(self):
        return self._rampTarget

    @property
    def isHeaterOn(self):
        return self._isHeaterOn

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
    def isPaused(self):
        return self._isPaused

    @property
    def limit(self):
        return self._limit

    @property
    def logMessage(self):
        return self._logMessage

    @direction.setter
    def direction(self, d):
        self._direction = d

    @isOutputModeTesla.setter
    def isOutputModeTesla(self, om):
        self._isOutputModeTesla = om

    @rampTarget.setter
    def rampTarget(self, rt):
        self._rampTarget = rt

    @isHeaterOn.setter
    def isHeaterOn(self, hs):
        self._isHeaterOn = hs

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

    @isPaused.setter
    def isPaused(self, p):
        self._isPaused = p

    @limit.setter
    def limit(self, lim):
        self._limit = lim

    @logMessage.setter
    def logMessage(self, lm):
        self._logMessage = lm

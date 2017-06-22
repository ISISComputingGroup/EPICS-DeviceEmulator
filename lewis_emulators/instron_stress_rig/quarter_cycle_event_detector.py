from quarter_cycle_event_detector_states import QuarterCycleEventDetectorStates as QCEDStates


class QuarterCycleEventDetector(object):

    def __init__(self):
        self.counts = 0
        self.max_counts = 0
        self.state = QCEDStates.PREPARED

    def reset(self):
        self.__init__()

    def arm(self):
        self.state = QCEDStates.ARMED

    def count(self):
        if self.state == QCEDStates.ARMED:
            self.counts += 1
            # This is intentionally == not >=. The counter won't trip if it already exceeds max_counts
            if self.counts == self.max_counts:
                self.state == QCEDStates.TRIPPED

    def off(self):
        self.state = QCEDStates.OFF
        self.counts = 0

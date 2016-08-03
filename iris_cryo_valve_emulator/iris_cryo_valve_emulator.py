import sys
sys.path.append("../test_framework")

from telnet_engine import TelnetEngine

class CryValveEmulator:
	
	CLOSED = "CLOSED"
	OPEN = "OPEN"
	
	def __init__(self):
		self.state = CryValveEmulator.CLOSED
		
	def process(self, data):
		if data == 'CLOSE':
			self.state = CryValveEmulator.CLOSED
			return ""
			
		if data == 'OPEN':
			self.state = CryValveEmulator.OPEN
			return ""
			
		if data == '?':
			return "SOLENOID " + self.state
		
		return None
		
		
if __name__ == "__main__":
	port_file = __file__
	dev = CryValveEmulator()
	TelnetEngine().start(dev, port_file)




import sys
sys.path.append("../test_framework")

from telnet_engine import TelnetEngine

class CryValveEmulator:
	
	CLOSED = "CLOSED"
	OPEN = "OPEN"
	TERMINATOR = "\r"
	
	def __init__(self):
		self.state = CryValveEmulator.CLOSED
		
	def process(self, data):
		if data == 'CLOSE':
			self.state = CryValveEmulator.CLOSED
			return CryValveEmulator.TERMINATOR
			
		if data == 'OPEN':
			self.state = CryValveEmulator.OPEN
			return CryValveEmulator.TERMINATOR
			
		if data == '?':
			return "SOLENOID " + self.state + CryValveEmulator.TERMINATOR
		
		return None
		
		
if __name__ == "__main__":
	port_file = __file__
	dev = CryValveEmulator()
	TelnetEngine().start(dev, port_file)




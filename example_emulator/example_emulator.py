import sys
sys.path.append("../test_framework")

from telnet_engine import TelnetEngine

class TemplateEmulator:
	def __init__(self):
		self.state = 0
		
	def process(self, data):
		if data == 'r_state':
			return 'state ' + str(int(self.state))
			
		if data.startswith('w_state'):
			self.state = data.split()[-1]
			return 'w_state 1'
		
		return None
		
		
if __name__ == "__main__":
	port_file = __file__
	dev = TemplateEmulator()
	TelnetEngine().start(dev, port_file)




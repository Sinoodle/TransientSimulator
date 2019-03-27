
#simple element container

class element:

	RES = 'R'
	IND = 'L'
	VCC = 'V'
	ICC = 'I'
	
	def __init__(self,name="None"):
		self.name = name
		self.pos_node = 0
		self.neg_node = 0
		self.value = 0
		self.type = element.RES
	
	def set_nodes(self,pnode,nnode):
		self.pos_node = pnode
		self.neg_node = nnode
		


def read_netlist(file_name):

	fin = open(file_name,'r')
	title = fin.readline()

	for line in fin:
	
		line = line.strip() # remove leading and trailing white space
		
		s = line[0].upper()
		
		if s == 'V':
			e = parse_voltage(line)
		elif  s == 'C':
			e = parse_capacitance(line)
		elif s == 'L' :
			e = parse_induction(line)
		elif s == 'I':
			e = parse_current(line)
		elif s == 'R':
			e = parse_resistor(line)
		else:
			print("Unknown Command or Element Description: " + line )
			e = None
		
		

def parse_voltage(text):



		

		
	
	
	




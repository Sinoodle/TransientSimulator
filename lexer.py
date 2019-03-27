""" Simple Lexer to Tokenize a given line in a circuit file """

class token:

	INT = "int"
	REAL = "real"
	STRING = "string"
	UNIT = "unit"
	EQUAL = "="
	
	def __init__(self):
		self.type = ""
		self.value = None
		

def eat_ws(text):

	index = 0
	while text[index] == string.whitespace:
		index = index + 1
		
	return text[index:]
	
def tolkenize(text):
	pass
#Text scanner for our .cir file
#Author: Jason Millard


"""

Things we scan for:

1. ID or Variable Names
2. Decimal Numbers, including floating point and floating point with scale factors ( 200k )
3. '*' and ';' each of these will cause ignore to EOL

"""

import string
import sys


token_delim = ' \t'
scales = "FPNUMKGT"
id_chars = string.ascii_letters + string.digits + "_"


def is_whitespace(char):
	if char in string.whitespace:
		return True
	else:
		return False

class token:

	#types of tokens
	NONE = 0
	EOL = 1
	ID = 2 # variable names
	DECIMAL = 3 # a base 10 number
	PERIOD = 4  # decimal point, must be followed by a decimal number
	EXP = 5  # E or e, should be precede by decimal or '.' and followed by sign or decimal
	EQU = 6 #equal sign
	SIGN = 7   # +/-
	ALPHADECIMAL = 8 # decimal followed a string of letters
	FLOAT = 9
	NUMBER = 10
	LINE_CONT = 11
	
	def __init__(self,type):
		self.type = type
		self.text = None
		self.scale = None
		self.desc = None
		
	def __str__(self):
		pass



class scanner:

	def __init__(self,filename):
		self.text = scanner.load_file(file)
		self.index = 0
		self.current_line = 1
		self.current_col = 0
		self.end = len(self.text) - 1
		self.start_of_line = True
		self.tolken_list = []
		
	def load_file(filename):
	
		with open(filename) as fin:
			fin.readline() # throw out title line
			return fin.read() # read entire contents of file
			
	def get_char(self):
		return self.text[self.index]
		
	def peek_back(self,n):
	
		if index - n >=0:
			return self.text[index-n]
		else:
			return None
	
	def peek_ahead(self,n):
	
		if index+n > end:
			return None
		else:
			return self.text[self.index+n]
	
			
	def eat_whitespace(self):
		while self.get_char() == SPACE or self.get_char() == TAB:
			consume()
		self.start_of_line = False
	
	def consume(self):  # 'next' char
	
		if self.index == end:
			return None
		else:
			self.index += 1
			self.start_of_line = False
			self.current_col += 1
	
	def consume_line(self): # gobbles up chars from current location to end of line 
	
		while self.get_char() != '\r' or self.get_char() != '\n':
			self.consume()
		
			
	def consume_validate(self,char):
		if self.text[self.index] is not char:
			print("SCAN ERROR: Expecting -> " + char + " but got -> " + self.text[self.index])
			print("Aborting Scan")
			sys.exit()
		else:
			self.index += 1
			self.start_of_line = False
			self.current_col += 1
		
	def get_token_list(self):  # main loop for scanning and generating tokens, returns a list of tokens
		
		while self.index == end:
			
			self.eat_whitespace()
			
			char = self.get_char()
						
			#At this point we should be at the start of a token
			#We have a large number of tests, once we are sure we can 'guess' the token, we process it.
			if char.isalpha() or char == "_":
				self.token_list.append(self.processs_id( ))
			elif char == '+' and self.start_of_line:
				self.consume()
				self.token_list.append(TOKEN(LINE_CONT))
			elif char.isdigit() or char == '+' or char == '-' or char =='.':
				self.token_list.append(self.processs_number())
			elif char == '\r':
				self.consume()
				self.consume_validate('\n')
				self.token_list.append(token(EOL))
				self.start_of_line = True
				self.current_line += 1
				self.current_col = 0
			elif char == '\n':
				self.consume()
				self.token_list.append(token(EOL))
				self.start_of_line = True
				self.current_line += 1
				self.current_col = 0
			elif char == '=':
				self.consume()
				self.token_list.append(token(EQU))
			elif char == '*' and self.start_of_line:
				self.consume_line()
			elif char ==';':
				self.consume_line()
			else:
				print("You shouldn't see this!")
				sys.exit()
				
				
	def process_id(self):
	
		t = token(ID)
		t.text += self.get_char()
		self.consume()
		
		while self.get_char() in id_chars:
			t.text += self.get_char()
			self.consume
		
		return t
		
			
			
	"""
	Supports 2 formats of floating point. 
	
	Format A, no leading digits are required in front of decimal point. ( -.234, +.234E-45, )
	floatingPoint_A ::= ('+'|'-')? [0-9]* '.' [0-9]+ (('E'|'e')('+'|'-')?[0-9]+)? 
	
	Format B, no  trailing digits behind the decimal point required ( 23. , 23.E34, 23.34E-45 )
	floatingPoint_B ::= ('+'|'-')? [0-9]+ ('.' ([0-9]+)?)? (('E'|'e')('+'|'-')?[0-9]+)?
	
	"""
	
	def process_number(self):
		
		has_leading_digits = False # flag for hints on floating point type
				
		t = token(token.NUMBER)
		
		#This number has no leading digits or sign, that's ok, but it must have digits after the '.', if not flag scanner error
		if self.get_char() == '.':
			if self.peek_ahead(1).isdigit():
				
				t.text = self.get_char()
				self.consume()
			else:
				print("Scanner Error, Expecting Number after \'.\', but found  " +self.peek_ahead(1))
				sys.exit()
				
		# This number has a leading sign, but no leading digits, make sure there are digits after the '.'
		elif  self.get_char() == '+' or self.get_char() == '-'  
			if self.peek_ahead(1) == '.':
				if self.peek_ahead(2).isdigit
					
					t.text = self.get_char() + "0."
					self.consume()
					self.consume()
				else:
					print("Scanner Error, Expecting Number after \'.\', but found  " + self.peek_ahead(2))
					sys.exit()
			#this number has a leading sign, and leading digits, decimal point, trailing digits and exp are all optional
			elif self.peek_ahead(1).isdigit():
				t.text = self.get_char()
				self.consume()
				has_leading_digits = True
			else: # only a digit and '.' are valid after a sign
				print("Scanner Error, Expecting Number after sign, but found  " + self.peek_ahead(1))
				sys.exit()
		else: # we covered all the cases, except for the char being digit to start with
			has_leading_digit = True
		
		#at this point, we should be looking at a number, before or after the '.'
		while self.get_char().isdigit():
			t.text += self.get_char()
			self.consume()
		
		char = self.get_char()
		
		#if there's a space, we are done
		if char.isspace() :
			return t
		
		#take care of any trailing digits after the decimal point
		if char == '.' and has_leading_digits :
			t.text += char
			self.consume()
			
			while self.get_char().isdigit():
				t.text += self.get_char()
				self.consume()
		else:
			print("Scanner Error, To many decimal points. " + t.text )
			sys.exit()
		
		if self.get_char().isspace:
			return t
		
		#at this point we either have an exponent or scaling factor
		
		#check for exponent
		if self.get_char().upper() = 'E':
			t.text += 'E'
			self.consume()
			if self.get_char() in '+-':
				t.text += self.get_char()
				self.consume()
			while self.get_char.isdigit():
				t.text += self.get_char()
				self.consume()
			#At this point we shoul be done, check that the next char is white space
			if self.get_char().isspace():
				return t
			else:
				print("Scanner Error, Unexpected Non-White Space Following Exponent: " + t.text + self.get_char() )
				sys.exit()
		
		elif self.get_char().upper() in scales:
			# PITA, check for MEG vs just M ( milli )
			if self.get_char().upper() == 'M' and self.peek_ahead(1).upper() == 'E' and self.peek_ahead(2).upper() == 'G':
				t.scale = 'MEG'
				#ignore rest of text ie MegOhms
				while self.get_char().isalpa():
					self.consume()
				
			else:
				t.scale = self.get_char().upper()
				#ignore rest of test, ie kOhms
				while self.get_char().isalpa():
					self.consume()
		else:
			print("Scanner Error, Expected Scale Factor, instead found: " + self.get_char)
			sys.exit()
		
		return t
	
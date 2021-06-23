##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2021.06.23
## Description:    Data parsing/printing tools
## Notes:
## Updates:
def prettyHex(h, l=False):
	'''Returns a printable hex string.
h is a bytes type.
If l, return a list of hex strings instead of one long string'''
	toret=''
	for b in h[:-1]:
		toret+=f"0x{hex(b)[2:]:>02} "
	toret+=f"0x{hex(h[-1])[2:]:>02}"
	if l:
		return toret.split(' ')
	return toret

def splitByte(b):
	'''Converts single byte to bin str.
b input is an int (because when subscripting a single bytes data it returns an int)'''
	return f"{bin(b)[2:]:>08}"

def pretty(data, width=0):
	'''Pretty prints data.
width is number of cols to takeup.
Works best if width is odd.
colour is the colour of the data.'''
	toret=''
	half=' '*(width//2)
	colour=data.getColour()
	string=data.toStr().split('\n')
	text=data.getText()
	length=len(text)-1
	for s in range(length):
		toret+=f"{colour}{half}{text[s]}{half}\033[0m {string[s]}\n"
	toret+=f"{colour}{half}{text[length]}{half}\033[0m {string[length]}"
	return toret

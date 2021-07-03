##
## Author:  Owen Cocjin
## Version: 0.3
## Date:    2021.07.03
## Description:    Data parsing/printing tools
## Notes:
## Updates:
##  - Added revBytes (mostly used by RTAP data)
def prettyHex(h, l=False):
	'''Returns a printable hex string.
h is a bytes type.
If l, return a list of hex strings instead of one long string'''
	toret=''
	if h==b'':
		return ''
	for b in h[:-1]:
		toret+=f"0x{hex(b)[2:]:>02} "
	toret+=f"0x{hex(h[-1])[2:]:>02}"
	if l:
		return toret.split(' ')
	return toret
def prettyParagraph(h):
	'''Prints long strings of hex data.
h is a bytes object'''
	counter=0
	for b in h:
		print(f"0x{hex(b)[2:]:>02}", end='')
		counter+=1
		if counter%16==0:
			print()
			continue
		if counter%8==0:
			print(' ', end='')
		print(' ', end='')
	print()

def revBytes(l):
	'''Returns a reversed bytes object'''
	toret=list(l)
	toret.reverse()
	toret=''.join([f"{hex(i)[2:]:>02}" for i in toret])
	return bytes.fromhex(toret)
def convertSigned(i, b):
	'''Returns a signed int, if signed bit set.
i is the int to check.
b is the length of i in bytes.'''
	b=b*8
	bits=f"{bin(i)[2:]:>0{b}}"
	if bits[0]=='1':
		mask=1<<(b-1)
		return (i^mask)*-1
	return i

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

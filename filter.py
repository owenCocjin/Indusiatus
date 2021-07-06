##
## Author:  Owen Cocjin
## Version: 0.3
## Date:    2021.07.06
## Description:    Functions and definitions for print filter
## Notes:
##  - in sym_* functions, target is the user's filter input and value is the value pulled from the packets
## Updates:
##  - Fixed all sym_* functions.
##    A previous change to indusiatus.filterParse swapped the arguments for sym_*.
##    This update reflects that swap.
from DataTypes import segment_names, segment_objs, packet_names
def sym_not(value, target):
	'''target is not value'''
	if type(value)==list:
		return target not in value
	return target!=value
def sym_less(value, target):
	'''target less than value'''
	return target<value
def sym_great(value, target):
	'''target greater than value'''
	return target>value
def sym_only(value, target):
	'''target is equal to value'''
	if type(value)==list:
		return target in value
	return target==value


def dtype(dtype, bundle):
	'''Return the appropriate data based on datatype input'''
	frame=bundle[0]
	packet=bundle[1]

	if dtype=="A":  #Whole packet
		return frame.getRaw()
	elif dtype=="D":  #IP destination
		try:
			return packet_names.getDst_ip()
		except AttributeError:
			return 'x.x.x.x'
	elif dtype=="H":  #Header Name
		return [i.getName() for i in bundle]
	elif dtype=="L":  #Length of full data
		return len(frame.getRaw())
	elif dtype=="S":  #IP source
		try:
			return packet.getSrc_ip()
		except AttributeError:
			return 'x.x.x.x'
	return None


def checkFilter(f):
	'''Checks to see if the filter is valid or not.
Returns True if it is.'''
	#Only allow certain symbols with certain data types
	if len(f)<3:
		return False
	symbol=f[0]
	type=f[1]
	data=f[2:]
	if type in symbol_type[symbol]:
		return True
	return False

symbols={'!':sym_not,
'<':sym_less,
'>':sym_great,
'=':sym_only}
symbol_type={'!':"ADHLS",
'<':'L',
'>':'L',
'=':"ADHLS"}

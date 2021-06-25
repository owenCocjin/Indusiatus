##
## Author:  Owen Cocjin
## Version: 0.2
## Date:    2021.06.25
## Description:    Functions and definitions for print filter
## Notes:
## Updates:
##  - Updated 'G' in dtypes
from DataTypes import segment_names, segment_objs, packet_names
def sym_not(target, value):
	'''target is not value'''
	if type(value)==list:
		return target not in value
	return target!=value
def sym_less(target, value):
	'''target less than value'''
	return target<value
def sym_great(target, value):
	'''target greater than value'''
	return target>value
def sym_only(target, value):
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
		return packet_names.getDst_ip()
	elif dtype=="H":  #Header Name
		return [i.getName() for i in bundle]
	elif dtype=="L":  #Length of full data
		return len(frame.getRaw())
	elif dtype=="S":  #IP source
		return packet.getSrc_ip()
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

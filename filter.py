##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2021.06.20
## Description:    Functions and definitions for print filter
## Notes:
## Updates:
##  - Updated 'G' in dtypes
from DataTypes import segment_names, segment_objs, packet_names
def sym_not(target, value):
	'''target is not value'''
	return target!=value
def sym_less(target, value):
	'''target less than value'''
	return target<value
def sym_great(target, value):
	'''target greater than value'''
	return target>value
def sym_only(target, value):
	'''target is equal to value'''
	return target==value


def dtype(dtype, bundle):
	'''Return the appropriate data based on datatype input'''
	frame=bundle[0]
	packet=bundle[1]

	if dtype=="A":  #Whole packet
		return frame.getRaw()
	elif dtype=="D":  #IP destination
		return packet_names.getDst_ip()
	elif dtype=="G":  #Layer type exists. Normally a segment
		for i in bundle:
			if i.data_type=="SEG":
				return i.getName()
		return None
	elif dtype=="L":  #Length of full data
		return len(frame.getRaw())
	elif dtype=="P":  #Packet type
		return packet_names[frame.getType()]
	elif dtype=="S":  #IP source
		return packet.getSrc_ip()

	return None

symbols={'!':sym_not,
'<':sym_less,
'>':sym_great,
'=':sym_only}

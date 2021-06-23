##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2021.06.20
## Description:    Functions and definitions for print filter
from DataTypes import segment_names, packet_names
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
	if len(bundle)==2:  #No segment
		frame, packet=bundle
		segment=None
	elif len(bundle)==3:  #Segment exists
		frame, packet, segment=bundle
	else:
		return None

	if dtype=="A":  #Whole packet
		return frame.getRaw()
	elif dtype=="D":  #IP destination
		return packet_names.getDst_ip()
	elif dtype=="G":  #Segment type
		if segment==None:  #Don't test just pass
			return (True, 'SKIP')
		return segment_names[packet.getProto()]
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

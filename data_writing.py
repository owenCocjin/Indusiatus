##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2021.06.20
## Description:    Packet writing functions
def write_1(packet, proto, fd):
	'''Writes whole packet'''
	fd.write(packet.getRaw())

def write_2(packet, proto, fd):
	'''Writes whole segment'''
	fd.write(proto.getRaw())

def write_3(packet, proto, fd):
	'''Writes just the payload data'''
	fd.write(proto.getPayload())

write_funcs={'1':write_1,
'2':write_2,
'3':write_3}

##
## Author:  Owen Cocjin
## Version: 0.2
## Date:    2021.06.24
## Description:    Segment data structure
## Notes:
## Updates:
##  - Added data_type and name to all classes

from .datatools import splitByte, prettyHex
from .payloaddata import *
class ICMPSegment():
	def __init__(self, raw):
		'''Takes the raw packet'''
		self.raw=raw
		self.data_type="SEG"
		self.name="ICMP"
		self.type=raw[0]
		self.code=raw[1]
		self.icmp_checksum=int(raw[2:4].hex(),16)
		self.content=raw[4:]
		self.offset=1  #Used for compatibility; 4-byte blocks
		self.colour='\033[46m'
		self.txt_colour='\033[96m'
		self.text="ICMP"
		self.upper=GENERICPayload(self.content)  #For compatability
	def __str__(self):
		return self.toStr()

	def toStr(self):
		return f"""Type:          {hex(self.type)}
Code:          {hex(self.code)}
ICMP Checksum: {self.icmp_checksum}
Content:       {prettyHex(self.content[:8])}..."""

	def getRaw(self):
		return self.raw
	def setRaw(self, new):
		self.raw=new
	def getData_type(self):
		return self.data_type
	def setData_type(self, new):
		self.data_type=new
	def getName(self):
		return self.name
	def setName(self, new):
		self.name=new
	def getType(self):
		return self.type
	def setType(self, new):
		self.type=new
	def getCode(self):
		return self.code
	def setCode(self, new):
		self.code=new
	def getIcmp_checksum(self):
		return self.icmp_checksum
	def setIcmp_checksum(self, new):
		self.icmp_checksum=new
	def getContent(self):
		return self.content
	def setContent(self, new):
		self.content=new
	def getOffset(self):
		return self.offset
	def setOffset(self, new):
		self.offset=new
	def getColour(self):
		return self.colour
	def setColour(self, new):
		self.colour=new
	def getTxt_colour(self):
		return self.txt_colour
	def setTxt_colour(self):
		self.txt_colour=new
	def getText(self):
		return self.text
	def setText(self, new):
		self.text=new
	def getUpper(self):  #For compatability
		return self.upper
	def setUpper(self, new):  #For compatability
		self.upper=new
	def getLL(self):
		return (self.offset*4, self.upper)

class IGMPSegment():
	def __init__(self, raw):
		self.raw=raw
		self.data_type="SEG"
		self.name="IGMP"
		buff=splitByte(raw[0])
		self.version=int(buff[:4],2)
		self.type=int(buff[4:],2)
		self.unused=raw[1]
		self.igmp_checksum=int(raw[2:4].hex(),16)
		self.group_addr=f"{raw[4]}.{raw[5]}.{raw[6]}.{raw[7]}"
		self.offset=2  #Mandatory; Compatability
		self.colour='\033[46m'
		self.txt_colour='\033[96m'
		self.text="IGMP"
		self.upper=None  #Mandatory; Compatability
	def __str__(self):
		return self.toStr()

	def toStr(self):
		return f"""Version:       {self.version}
Type:          {self.type}
Group Addr:    [{self.group_addr}]
IGMP Checksum: {self.igmp_checksum}"""

	def getRaw(self):
		return self.raw
	def setRaw(self, new):
		self.raw=new
	def getData_type(self):
		return self.data_type
	def setData_type(self, new):
		self.data_type=new
	def getName(self):
		return self.name
	def setName(self, new):
		self.name=new
	def getVersion(self):
		return self.version
	def setVersion(self, new):
		self.version=new
	def getType(self):
		return self.type
	def setType(self, new):
		self.type=new
	def getUnused(self):
		return self.unused
	def setUnused(self, new):
		self.unused=new
	def getIgmp_checksum(self):
		return self.igmp_checksum
	def setIgmp_checksum(self, new):
		self.igmp_checksum=new
	def getGroup_addr(self):
		return self.group_addr
	def setGroup_addr(self, new):
		self.group_addr=new
	def getOffset(self):  #Compatability
		return self.offset
	def setOffset(self, new):  #Compatability
		self.offset=new
	def getColour(self):
		return self.colour
	def setColour(self, new):
		self.colour=new
	def getTxt_colour(self):
		return self.txt_colour
	def setTxt_colour(self):
		self.txt_colour=new
	def getText(self):
		return self.text
	def setText(self, new):
		self.text=new
	def getUpper(self):
		return self.upper
	def setUpper(self, new):
		self.upper=new
	def getLL(self):
		return (self.offset*4, self.upper)

class TCPSegment():
	def __init__(self, raw):
		'''Takes the raw packet'''
		self.raw=raw
		self.data_type="SEG"
		self.name="TCP"
		self.src_port=int(raw[0:2].hex(),16)
		self.dst_port=int(raw[2:4].hex(),16)
		self.seq_no=int(raw[4:8].hex(),16)
		self.ack_no=int(raw[8:12].hex(),16)
		buff=splitByte(raw[12])
		self.offset=int(buff[:4],2)  #Size of segment/4
		self.reserved=int(buff[4:],2)
		self.flags=splitByte(raw[13])
		self.window=int(raw[14:16].hex(),16)
		self.tcp_checksum=int(raw[16:18].hex(),16)
		self.urgent_pointer=raw[18:20]  #Not sure what this is ahahah
		self.colour='\033[46m'
		self.txt_colour='\033[96m'
		self.text="TCP"
		if self.offset>5:
			self.options=raw[20:(self.offset*4)]
		else:
			self.options=None
		self.payload=raw[self.offset*4:]
		self.pay_len=len(self.raw)-self.offset*4
		if self.pay_len!=0:
			self.upper=GENERICPayload(self.payload)  #Mandatory; Compatability (This should be replaced with payload)
		else:
			self.upper=None
	def __str__(self):
		return self.toStr()

	def toStr(self):
		return f"""Sequence:     {self.seq_no} ({self.ack_no}) | [{self.src_port}] -> [{self.dst_port}]
Length:       {self.pay_len}=Payload({self.pay_len})
TCP Checksum: {self.tcp_checksum}"""

	def getRaw(self):
		return self.raw
	def setRaw(self, new):
		self.raw=new
	def getData_type(self):
		return self.data_type
	def setData_type(self, new):
		self.data_type=new
	def getName(self):
		return self.name
	def setName(self, new):
		self.name=new
	def getSrc_port(self):
		return self.src_port
	def setSrc_port(self, new):
		self.src_port=new
	def getDst_port(self):
		return self.dst_port
	def setDst_port(self, new):
		self.dst_port=new
	def getSeq_no(self):
		return self.seq_no
	def setSeq_no(self, new):
		self.seq_no=new
	def getAck_no(self):
		return self.ack_no
	def setAck_no(self, new):
		self.ack_no=new
	def getOffset(self):
		return self.offset
	def setOffset(self, new):
		self.offset=new
	def getReserved(self):
		return self.reserved
	def setReserved(self, new):
		self.reserved=new
	def getFlags(self):
		return self.flags
	def setFlags(self, new):
		self.flags=new
	def getWindow(self):
		return self.window
	def setWindow(self, new):
		self.window=new
	def getTcp_checksum(self):
		return self.tcp_checksum
	def setTcp_checksum(self, new):
		self.tcp_checksum=new
	def getUrgent_pointer(self):
		return self.urgent_pointer
	def setUrgent_pointer(self, new):
		self.urgent_pointer=new
	def getPayload(self):
		return self.payload
	def setPayload(self, new):
		self.payload=new
	def getColour(self):
		return self.colour
	def setColour(self, new):
		self.colour=new
	def getTxt_colour(self):
		return self.txt_colour
	def setTxt_colour(self):
		self.txt_colour=new
	def getText(self):
		return self.text
	def setText(self, new):
		self.text=new
	def getUpper(self):
		return self.upper
	def setUpper(self, new):
		self.upper=new
	def getLL(self):
		return (self.offset*4, self.upper)

class UDPSegment():
	'''Takes the raw packet.
Assumes no IP header exists.'''
	def __init__(self, raw):
		self.raw=raw
		self.data_type="SEG"
		self.name="UDP"
		self.src_port=int(raw[:2].hex(),16)
		self.dst_port=int(raw[2:4].hex(),16)
		self.length=int(raw[4:6].hex(),16)  #Length includes UDP header
		self.udp_checksum=int(raw[6:8].hex(),16)
		self.offset=8  #Constant 8 bytes
		self.colour='\033[46m'
		self.txt_colour='\033[96m'
		self.text="UDP"
		self.payload=raw[self.offset:]
		if self.length-8>0:
			self.upper=GENERICPayload(self.payload)  #Mandatory; Compatability
		else:
			self.upper=None
	def __str__(self):
		return self.toStr()

	def toStr(self):
		return f"""Source->Dest: [{self.src_port}] -> [{self.dst_port}]
Length: {self.length}-8=Payload({self.length-8})
UDP Checksum: {self.udp_checksum}"""

	def getRaw(self):
		return self.raw
	def setRaw(self, new):
		self.raw=new
	def getData_type(self):
		return self.data_type
	def setData_type(self, new):
		self.data_type=new
	def getName(self):
		return self.name
	def setName(self, new):
		self.name=new
	def getSrc_port(self):
		return self.src_port
	def setSrc_port(self, new):
		self.src_port=new
	def getDst_port(self):
		return self.dst_port
	def setDst_port(self, new):
		self.dst_port=new
	def getLength(self):
		return self.length
	def setLength(self, new):
		self.length=new
	def getUdp_checksum(self):
		return self.udp_checksum
	def setUdp_checksum(self, new):
		self.udp_checksum=new
	def getOffset(self):  #Mandatory; Compatability
		return self.offset
	def getColour(self):
		return self.colour
	def setColour(self, new):
		self.colour=new
	def getTxt_colour(self):
		return self.txt_colour
	def setTxt_colour(self):
		self.txt_colour=new
	def getText(self):
		return self.text
	def setText(self, new):
		self.text=new
	def getPayload(self):
		return self.payload
	def setPayload(self, new):
		self.payload=new
	def getUpper(self):
		return self.upper
	def setUpper(self, new):
		self.upper=new
	def getLL(self):
		return (self.offset*4, self.upper)

'''
|||    DEMO    |||
'''
class PROTOSegment():
	'''Everything required by a segment object.
Everything here must be overwritten!'''
	def __init__(self, raw):
		self.raw=raw
		self.offset=None  #Int division by 4; Size of header
		self.colour=None
		self.txt_colour=None
		self.text=None

	def getRaw(self):
		return self.raw
	def setRaw(self, new):
		self.raw=new
	def getOffset(self):
		return self.offset
	def setOffset(self, new):
		self.offset=new
	def getColour(self):
		return self.colour
	def setColour(self, new):
		self.colour=new
	def getTxt_colour(self):
		return self.txt_colour
	def setTxt_colour(self, new):
		self.txt_colour=new
	def getText(self):
		return self.text
	def setText(self, new):
		self.text=new


'''
|||    DICTS    |||
'''

segment_names={1:"ICMP",
2:"IGMP",
6:"TCP",
9:"IGRP",
17:"UDP",
47:"GRE",
50:"ESP",
51:"AH",
57:"SKIP",
58:"ICMP",
88:"EIGRP",
89:"OSPF",
115:"L2TP"}
segment_objs={"TCP":TCPSegment,
"UDP":UDPSegment,
"ICMP":ICMPSegment,
"IGMP":IGMPSegment}

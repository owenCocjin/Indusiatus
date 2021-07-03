##
## Author:  Owen Cocjin
## Version: 0.4
## Date:    2021.07.03
## Description:    Frame data structure
## Notes:
##  - pretty() loops as many times as the length of self.text
## Updates:
##  - Added RTAPFrame class

from .packetdata import *
from .payloaddata import GENERICPayload
from .datatools import prettyHex, revBytes, prettyParagraph
from .Radiotap import *
class ETHFrame():
	def __init__(self, raw):
		'''Socket removes preamble SFD, and CRC footer (12 bytes total) from data.'''
		self.raw=raw
		self.data_type="ETH"
		self.name="ETH"
		dst=raw[:6].hex()
		src=raw[6:12].hex()
		self.dst_mac=':'.join([dst[b*2:b*2+2] for b in range(len(dst)//2)])
		self.src_mac=':'.join([src[b*2:b*2+2] for b in range(len(src)//2)])
		self.type=int(raw[12:14].hex(),16)  #Type of packet data
		self.payload=raw[14:]
		self.upper=packet_types[self.type](self.payload)
		self.width_inc=True  #Increment my width if needed
		self.colour='\033[45m'
		self.txt_colour='\033[95m'
		self.text="ETH"
		# self.packet=IPPacket(self.payload)
	def __str__(self):
		return self.toStr()

	def toStr(self):
		return f"""Source MAC: [{self.src_mac}]
Dest MAC:   [{self.dst_mac}]
Type:       {hex(self.type)}({packet_names[self.type]})"""

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
	def getDst_mac(self):
		return self.dst_mac
	def setDst_mac(self, new):
		self.dst_mac=new
	def getSrc_mac(self):
		return self.src_mac
	def setSrc_mac(self, new):
		self.src_mac=new
	def getType(self):
		return self.type
	def setType(self, new):
		self.type=new
	def getPayload(self):
		return self.payload
	def setPayload(self, new):
		self.payload=new
	def getUpper(self):
		return self.upper
	def setUpper(self, new):
		self.upper=new
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
	def getWidthInc(self):
		return self.width_inc
	def setWidthInc(self, new):
		self.width_inc=new
	def getLL(self):
		return (14, self.upper)

class RTAPFrame():
	'''RadioTap headers are little endien order!'''
	def __init__(self, raw):
		self.raw=raw
		self.data_type="RTAP"
		self.name="RTAP"
		self.revision=raw[0]
		self.padding=raw[1]  #Used to align bytes
		self.length=int(revBytes(raw[2:4]).hex(),16)  #Header length
		self.present_list,self.present_data=parsePresents(raw)
		self.payload=raw[self.length:]
		self.upper=RTAPPacket(self.present_list, self.present_data, self.payload)
		self.colour='\033[45m'
		self.txt_colour='\033[95m'
		self.width_inc=True
		self.text="RAD"
	def __str__(self):
		return self.toStr()

	def toStr(self):
		toret=f"""
Length: {self.length}
"""
		return toret
	def getBmapLen(self):
		'''Determines the length of the bitmap both as the length of the list and the total bytes.'''
		toret=0
		for b in self.bitmap:
			toret+=b.getSize()
		return (len(self.bitmap),toret)

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
	def getRevision(self):
		return self.revision
	def setRevision(self, new):
		self.revision=new
	def getPadding(self):
		return self.padding
	def setPadding(self, new):
		self.padding=new
	def getLength(self):
		return self.length
	def setLength(self, new):
		self.length=new
	def getPresent(self):
		return self.present
	def setPresent(self, new):
		self.present=new
	def getPayload(self):
		return self.payload
	def setPayload(self, new):
		self.payload=new
	def getUpper(self):
		return self.upper
	def setUpper(self, new):
		self.upper=new
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
	def getWidthInc(self):
		return self.width_inc
	def setWidthInc(self, new):
		self.width_inc=new
	def getLL(self):
		return (self.length, self.upper)

frame_names={"ETH":ETHFrame,
"RTAP":RTAPFrame}

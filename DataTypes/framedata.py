##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2021.06.22
## Description:    Frame data structure
## Notes:
## Updates:
from .packetdata import *
from .datatools import prettyHex
class ETHFrame():
	def __init__(self, raw):
		'''Socket removes preamble SFD, and CRC footer (12 bytes total) from data.'''
		self.raw=raw
		dst=raw[:6].hex()
		src=raw[6:12].hex()
		self.dst_mac=':'.join([dst[b*2:b*2+2] for b in range(len(dst)//2)])
		self.src_mac=':'.join([src[b*2:b*2+2] for b in range(len(src)//2)])
		self.type=int(raw[12:14].hex(),16)  #Type of packet data
		self.payload=raw[14:]
		self.upper=packet_types[self.type](self.payload)
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
	def getLL(self):
		return (14, self.upper)

##
## Author:  Owen Cocjin
## Version: 0.3
## Date:    2021.06.24
## Description:    IPv6 extension header classes
## Notes:
##  - Figure out how options work.
##    Will probably just print them on a line with HbH instead of cluttering pretty output
## Updates:
##  - Made Exts check segment list for next headers
##  - Added data_type and name to all classes

from .datatools import prettyHex
from .segmentdata import *
class HBHExt():
	def __init__(self, raw):
		self.raw=raw
		self.data_type="EXT"
		self.name="HBH"
		self.next_hdr=raw[0]
		self.hel=raw[1]  #Header Extension Lenght; 8-byte blocks not including first 8 bytes
		self.content=raw[2:8*(self.hel+1)]
		self.payload=raw[8*(self.hel+1):]
		if self.next_hdr in segment_names:
			self.upper=segment_objs[segment_names[self.next_hdr]](self.payload)
		elif self.next_hdr in ext_header_names:
			self.upper=ext_headers[ext_header_names[self.next_hdr]](self.payload)
		self.colour='\033[41m'
		self.txt_colour='\033[91m'
		self.text="HbH"
	def __str__(self):
		return self.toStr()

	def toStr(self):
		return f"""Next Header:        {self.next_hdr}
Header Ext. Length: {self.hel}
No. of Options:     {len(self.option)}"""

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
	def getNext_hdr(self):
		return self.next_hdr
	def setNext_hdr(self, new):
		self.next_hdr=new
	def getHel(self):
		return self.hel
	def setHel(self, new):
		self.hel=new
	def getContent(self):
		return self.content
	def setContent(self, new):
		self.content=new
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

'''
|||    DICTS    |||
'''
ext_header_names={0:"hop-by-hop"}
#43:"routing",
#44:"fragment",
#51:"auth",
#50:"esp",
#60:"destination",
#135:"mobility",
#139:"host",
#140:"shim6"}
ext_headers={"hop-by-hop":HBHExt}  #Most common
#"destination":DSTExt,  #MIGHT OCCURE TWICE
#"routing":ROUTEExt,
#"fragment":FRAGMENTExt,
#"auth":AUTHExt,
#"esp":ESPExt,  #Encapsulating Security Payload
#"host":HOSTIDExt,
#"shim6":SHIM6Ext}

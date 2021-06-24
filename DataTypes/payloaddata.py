##
## Author:  Owen Cocjin
## Version: 0.2
## Date:    2021.06.24
## Description:    Payload data structured
## Notes:
##    - Includes a generic payload class
## Updates:
##  - Added data_type and name to all classes

class GENERICPayload():
	def __init__(self, raw):
		self.raw=raw
		self.data_type="PAY"
		self.name="GENERIC"
		self.upper=None
		self.length=len(raw)  #Length in bytes
		self.colour='\033[43m'
		self.txt_colour='\033[93m'
		self.text="PAY"
	def __str__(self):
		return self.toStr()

	def toStr(self):
		return f"""
Length: {self.length}
"""

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
	def getLL(self):
		return (self.length, self.upper)


payloads={"generic":GENERICPayload}

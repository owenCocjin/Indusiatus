##
## Author:  Owen Cocjin
## Version: 0.5
## Date:    2021.07.12
## Description:    Functions and definitions for print filter
## Notes:
##  - In sym_* functions, target is the user's filter input and value is the value pulled from the packets
##  - To add a new filter parameter, add dtype to Filter.dtypes and adjust symbol_type as needed
## Updates:
##  - Added a Filter class which allows for a more dynamic approach to parsing filters
##  - Fixed issue with setting length during Filter.setRaw()
##  - Fixed sym_less and sym_great being backwards
##  - Added mac and port filters
class Filter():
	def __init__(self):
		self.raw=None
		self.length='0'
		self.headers=[]
		self.src_mac=None
		self.dst_mac=None
		self.src_ip=None
		self.dst_ip=None
		self.src_port=None
		self.dst_port=None
		self.dtypes={'A':self.getRaw,
'D':self.getDst_ip,
'H':self.getHeaders,
'L':self.getLength,
'M':self.getSrc_mac,
'N':self.getDst_mac,
'P':self.getSrc_port,
'Q':self.getDst_port,
'S':self.getSrc_ip}
	def __str__(self):
		return f"{self.__dict__}"

	def dtype(self, value):
		return self.dtypes[value]()
	def wipe(self):
		'''Resets all values'''
		self.raw=None
		self.length=0
		self.headers.clear()
		self.src_mac=None
		self.dst_mac=None
		self.src_ip=None
		self.dst_ip=None
		self.src_port=None
		self.dst_port=None
	def macs(self, s, d):
		self.src_mac=s
		self.dst_mac=d
	def ips(self, s, d):
		self.src_ip=s
		self.dst_ip=d
	def ports(self, s, d):
		self.src_port=s
		self.dst_port=d

	def getRaw(self):
		return self.raw
	def setRaw(self, new):
		self.raw=new
		self.length=len(self.raw)
	def getLength(self):
		return self.length
	def setLength(self, new):
		self.length=new
	def getHeaders(self):
		return self.headers
	def setHeaders(self, new):
		self.headers=new
	def addHeader(self, new):
		self.headers.append(new)
	def getSrc_mac(self):
		return self.src_mac
	def setSrc_mac(self, new):
		self.src_mac=new
	def getDst_mac(self):
		return self.dst_mac
	def setDst_mac(self, new):
		self.dst_mac=new
	def getSrc_ip(self):
		return self.src_ip
	def setSrc_ip(self, new):
		self.src_ip=new
	def getDst_ip(self):
		return self.dst_ip
	def setDst_ip(self, new):
		self.dst_ip=new
	def getSrc_port(self):
		return self.src_port
	def setSrc_port(self, new):
		self.src_port=new
	def getDst_port(self):
		return self.dst_port
	def setDst_port(self, new):
		self.dst_port=new

def sym_not(value, target):
	'''target is not value'''
	if type(value)==list:
		return target not in value
	return target!=value
def sym_less(value, target):
	'''target less than value'''
	return value<target
def sym_great(value, target):
	'''target greater than value'''
	return value>target
def sym_only(value, target):
	'''target is equal to value'''
	if type(value)==list:
		return target in value
	return target==value

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
symbol_type={'!':"ADHLMNPQS",
'<':'LPQ',
'>':'LPQ',
'=':"ADHLMNPQS"}

#Global filter object.
#Each header class will edit this object as needed.
FILTER=Filter()

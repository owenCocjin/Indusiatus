#!/usr/bin/python3
## Author:  Owen Cocjin
## Version: 0.6
## Date:    2021.07.06
## Description:    Packet capturer
## Notes:
##  - Need to fix IPv6 and it's stupid header shieeee!
##  - Also would like to know how to test IPv6 stuff
## Updates:
##  - Updated filterParse to print value of filter when using verbose printing.
from ProgMenu.progmenu import MENU
from datawriting import writeData
import DataTypes as dtypes
import menuentries, filter
import socket, time
vprint=MENU.verboseSetup(['v', "verbose"])
PARSER=MENU.parse(True, strict=True)
vname=__file__[__file__.rfind('/')+1:-3]
total_cap=[-1]  #Total captured packets

def main():
	vprint(f"[|X:{vname}:PARSER]: {PARSER}")
	print(f"[|X:{vname}]: Starting up...")
	#Check errors
	if PARSER["output"]==False:  #Explicitely False; Not called returns None
		print(f"[|X:{vname}]: Couldn't write to output file! Either the layer flag is missing or the file is unaccessible.")
		exit(1)
	if PARSER["frame"] not in dtypes.frame_names:
		print(f"[|X:{vname}:setup]: Invalid frame type passed: '{PARSER['frame']}'!")
		exit(3)
	vprint(f"[|X:{vname}]: Setting up raw socket...")
	sock=socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x03))  #The 3 is to read all data, incoming & outgoing
	try:
		sock.bind((PARSER["host"], 0))
	except OSError as e:
		print(f"[|X:{vname}:Binding]: Interface {PARSER['host']} doesn't exist!")
		exit(4)
	vprint(f"[|X:{vname}:setup]: Configuring printing type...")
	if not any((PARSER["raw"], PARSER["short"])):
		PARSER["pretty"]=True
	if PARSER["short"]:
		printData=shortPrint
	else:
		printData=dataPrint

	print(f"[|X:{vname}]: Listening...")
	if PARSER["dump"]:
		#Dump packets; Used for testing with unknown data
		while True:
			buff, cli=sock.recvfrom(65535)
			print(f"[|X:{vname}:dump]: Got {len(buff)} bytes from {cli[0]}!")
			dtypes.prettyParagraph(buff)
	#Filtered loop
	elif PARSER["filter"]!=None:
		vprint(f"[|X:{vname}]: Filtering...")
		#Check filters
		badfilter=False
		for f in PARSER["filter"]:
			if not filter.checkFilter(f):
				print(f"[|X:{vname}:filter]: Bad filter found: '{f}'!")
				badfilter=True
		if badfilter:
			exit(2)
		while True:
			buff, bundle, cli=setup(sock)
			if filterParse(buff, bundle):
				incCap()
				printData(bundle)
				if PARSER["output"]:
					writeData(PARSER["output"], bundle, PARSER["layer"])
	else:
		while True:
			try:
				buff, bundle, cli=setup(sock)
			except KeyError as e:
				input(f"[|X:{vname}:KeyError]: {e}. Press enter to continue...")
				continue
			incCap()
			printData(bundle)
			if PARSER["output"]:
				writeData(PARSER["output"], bundle, PARSER["layer"])

def setup(sock):
	'''Does all the setup.'''
	buff, cli=sock.recvfrom(65565)
	bundle=(dtypes.frame_names[PARSER["frame"]](buff),)  #This always exists
	bundle+=(bundle[-1].getUpper(),)  #There should always be a second layer
	while bundle[-1].getUpper()!=None:
		bundle+=(bundle[-1].getUpper(),)
	return buff, bundle, cli
def shortPrint(data):
	'''Print all data in a row'''
	print(f"\033[100m[{time.strftime('%Y.%m.%d|%H:%M:%S')}]({getCap()})\033[0m ", end='')
	for d in data:
		print(f"{d.getColour()}{d.getName()} ", end='')
	print('\033[0m')
def dataPrint(data):
	'''data is a tuple:(frame, packet, [segment])'''
	print(f"\n    \033[100m[{time.strftime('%Y.%m.%d|%H:%M:%S')}]\n[|X:{vname}:raw_socket]: Read {len(data[0].getRaw())} bytes! ({getCap()})\033[0m")
	if PARSER["pretty"]:
			# toprnt_packet=packet.toStr().split('\n')
			# toprnt_segment=segment.toStr().split('\n')
			# toprnt_packet=packet.toStr().replace('\n', '\n \033[44m \033[0m')
			# toprnt_segment=segment.toStr().replace('\n','\n \033[46m \033[0m   ')
			counter=1
			for d in data:
				print(dtypes.pretty(d,counter))
				counter+=2

	if PARSER["raw"]:
		'''Treat each layer as a chain'''
		counter=0
		bytes=0
		raw=data[0].getRaw()
		print('\033[100m0x0000\033[0m ', end='')
		for d in data:
			length=d.getLL()[0]
			print(f"{d.getTxt_colour()}", end='')
			for h in dtypes.prettyHex(d.getRaw()[:length], l=True):
				print(f"{h} ", end='')
				counter+=1
				if counter%16==0:
					bytes+=16
					print(f"\n\033[0m\033[100m0x{hex(bytes)[2:]:>04}\033[0m {d.getTxt_colour()}", end='')
				elif counter%8==0:
					print(' ', end='')
		print('\033[0m')

def filterParse(buff, bundle):
	'''Return True if contents pass the filter'''
	bundle_classes=[type(b) for b in bundle]
	for f in PARSER["filter"]:
		symbol=f[0]
		datatype=filter.dtype(f[1].upper(), bundle)  #Raw packet data
		value=f[2:]  #User passed filter value
		vprint(f"\n[|X:{vname}:filterParse]: Filter: {f}({value}) vs {datatype}... ", end='')

		if f[1] in "L":
			try:
				value=int(value)
			except ValueError:
				print(f"[|X:{vname}:filterParse]: Bad filter value given!")
				exit(2)
		if datatype!=None and filter.symbols[symbol](datatype, value):
			vprint("Passed", end='')
			continue
		else:
			vprint("Failed", end='')
			return False
	return True
def incCap():
	'''Increment global cap counter'''
	total_cap[0]+=1
def getCap():
	return f"0x{hex(total_cap[0])[2:]:>04}"


if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt:
		if PARSER["output"]:
			PARSER["output"].close()
		print("\r\033[K\033[0m", end='')

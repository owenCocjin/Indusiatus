#!/usr/bin/python3
## Author:  Owen Cocjin
## Version: 0.3
## Date:    2021.06.25
## Description:    Packet capturer
## Notes:
##  - Need to fix IPv6 and it's stupid header shieeee!
##  - Also would like to know how to test IPv6 stuff
## Updates:
##  - Checks for invalid filters
from ProgMenu.progmenu import MENU
from data_writing import writeData
import DataTypes as dtypes
import menuentries, filter
import socket, time
vprint=MENU.verboseSetup(['v', "verbose"])
PARSER=MENU.parse(True, strict=True)
vname=__file__[__file__.rfind('/')+1:-3]
def main():
	vprint(f"[|X:{vname}:PARSER]: {PARSER}")
	print(f"[|X:{vname}]: Starting up...")
	if PARSER["output"]==False:  #Explicitely False; Not called returns None
		print(f"[|X:{vname}]: Couldn't write to output file! Either the layer flag is missing or the file is unaccessible.")
		exit(1)
	vprint(f"[|X:{vname}]: Setting up raw socket...")
	sock=socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x03))  #The 3 is to read all data, incoming & outgoing
	sock.bind((PARSER["host"], 0))

	print(f"[|X:{vname}]: Listening...")
	#Filtered loop
	if PARSER["filter"]!=None:
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
			# try:
			buff, bundle, cli=setup(sock)
			# except KeyError as e:
			# 	input(f"[|X:{vname}:KEYERROR]: {e}")
			# 	continue
			if filterParse(buff, bundle):
				print(f"\n    \033[100m[{getTime()}]\n[|X:{vname}:raw_socket]: Read {len(buff)} bytes from dev({cli[0]})! \033[0m")
				printData(bundle)
				if PARSER["output"]:
					writeData(PARSER["output"], bundle, PARSER["layer"])
	else:
		while True:
			try:
				buff, bundle, cli=setup(sock)
				print(f"\n    \033[100m[{getTime()}]\n[|X:{vname}:raw_socket]: Read {len(buff)} bytes from dev({cli[0]})! \033[0m")
			except KeyError as e:
				input(f"KEYERROR: {e}")
				continue
			printData(bundle)
			if PARSER["output"]:
				writeData(PARSER["output"], bundle, PARSER["layer"])

def setup(sock):
	'''Does all the setup.'''
	buff, cli=sock.recvfrom(65565)
	bundle=(dtypes.ETHFrame(buff),)  #This always exists
	bundle+=(bundle[-1].getUpper(),)  #There should always be a second layer
	while bundle[-1].getUpper()!=None:
		bundle+=(bundle[-1].getUpper(),)
	return buff, bundle, cli
def printData(data):
	'''data is a tuple:(frame, packet, [segment])'''
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
		datatype=filter.dtype(f[1].upper(), bundle)
		value=f[2:]
		vprint(f"\n[|X:{vname}:filterParse]: Filter: {f} vs {datatype}... ", end='')

		if f[1] in "L":
			try:
				value=int(value)
			except ValueError:
				print(f"[|X:{vname}:filterParse]: Bad filter value given!")
				exit(2)
		if datatype!=None and filter.symbols[symbol](value, datatype):
			vprint("Passed", end='')
			continue
		else:
			vprint("Failed", end='')
			return False
	return True

def getTime():
	t=time.localtime()
	return f"{t.tm_year}.{t.tm_mon}.{t.tm_mday}/{t.tm_hour}:{t.tm_min}:{t.tm_sec}"


if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt:
		if PARSER["output"]:
			PARSER["output"].close()
		print("\r\033[K", end='')

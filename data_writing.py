##
## Author:  Owen Cocjin
## Version: 0.2
## Date:    2021.06.24
## Description:    Packet writing functions
from ProgMenu.progmenu import MENU
vprint=MENU.verboseSetup(['v', "verbose"])
vname=__file__[__file__.rfind('/')+1:-3]
def writeData(fd, data, layer=0):
	'''Write raw data to fd.
layer is the layer of data to write.
If layer is larger than the size the data tuple, no data will be written'''
	if layer<=len(data)-1:
		towrite=data[layer].getRaw()
		vprint(f"[|X:{vname}:writeData]: Writing {data[layer].getText().strip()}")
		fd.write(b'\x3b')
		fd.write(bytes.fromhex(f"{hex(len(towrite))[2:]:>04}"))
		fd.write(b'\x3b')
		fd.write(towrite)
		fd.flush()
		vprint(f"[|X:{vname}:writeData]: Success!")
		return True
	else:
		vprint(f"[|X:{vname}:writeData]: Layer doesn't exist!")
	return False

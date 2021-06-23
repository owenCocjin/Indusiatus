##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2021.06.23
## Description:    Menu entries for progmenu
from ProgMenu.progmenu import EntryFlag, EntryArg

def filterFunc(f):
	'''Filter what to print.
Split args with semi-colon.'''
	return f.split(';')
def helpFunc():
	print('''    evildict.py [-h]
MitM attack to modify a dictionary return to slate quizzes.
  -f; --filter=<sTv>: Filter print results.
                      Syntax is: <s><t><v>
                        <s>: Comparison symbol:
                          - !: Not equal
                          - =: Exactly equal
                          - <: Less than
                          - >: Greater than
                        <t>: Data type as a single letter:
                          - A: Data (packet as a whole)
                          - D: IP destination
                          - G: Segment type
                          - L: Packet length
                          - P: Packet type
                          - S: IP source
                        <v>: Value, such as the IP, data length, etc...
  -h; --help:         Prints this page
  -l; --layer=<l>;    Determines TCP/IP layer to output:
                        - 1: Internet Headers + Payload
                        - 2: Transport Headers + Payload
                        - 3: Payload (no headers)
                      Must be used in conjunction with --output.
  -o; --output=<file>; Writes output to <file>.
                      Must use with --layer.
                      Overwrites existing files.
  -p; --pretty;       Formatted printing
  -r; --raw:          Print the raw packet bytes''')
    #-i; --ip:           Include the IP header
	return True
def outputFunc(l, o):
	'''Returns output file if it exists, otherwise False'''
	if l in "123":
		return open(o, 'wb')
	else:
		return False

EntryArg("host", ['a', "host"], lambda a:str(a), strict=True)
EntryArg("filter", ['f', "filter"], filterFunc)
EntryFlag("help", ['h', "help"], helpFunc)
#EntryFlag("ip", ['i', "ip"], lambda:True, default=False)
EntryArg("layer", ['l', "layer"], lambda l:l)
EntryArg("output", ['o', "output"], outputFunc, recurse=["layer"])
EntryFlag("pretty", ['p', "pretty", "formatted"], lambda:True)
EntryFlag("raw", ['r', "raw"], lambda:True, default=False)

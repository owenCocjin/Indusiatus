##
## Author:  Owen Cocjin
## Version: 0.4
## Date:    2021.06.25
## Description:    Menu entries for progmenu
## Updates:
##  - Replaced filters 'G' and 'P' with 'H'
from ProgMenu.progmenu import EntryFlag, EntryArg

def filterFunc(f):
	'''Filter what to print.
Split args with semi-colon.'''
	return f.split(';')
def helpFunc():
	print('''    evildict.py -a <host device> [-fhlopr]
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
                          - H: Header type (IPV6, HBH, ICMP, etc...)
                          - L: Frame length
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
  -r; --raw:          Print the raw packet bytes
Output Files:
  When writing output, the raw bytes will be preceded with the 4 bytes combo of:
    0x3b 0xss 0xss 0x3b
  Where 0xss is the total size of the written bytes.''')
    #-i; --ip:           Include the IP header
	return True
def outputFunc(l, o):
	'''Returns output file if it exists, otherwise False'''
	return open(o, 'wb')

EntryArg("host", ['a', "host"], lambda a:str(a), strict=True)
EntryArg("filter", ['f', "filter"], filterFunc)
EntryFlag("help", ['h', "help"], helpFunc)
#EntryFlag("ip", ['i', "ip"], lambda:True, default=False)
EntryArg("layer", ['l', "layer"], lambda l:int(l), default=0)
EntryArg("output", ['o', "output"], outputFunc, recurse=["layer"])
EntryFlag("pretty", ['p', "pretty", "formatted"], lambda:True)
EntryFlag("raw", ['r', "raw"], lambda:True, default=False)

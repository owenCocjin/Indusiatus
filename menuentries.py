##
## Author:  Owen Cocjin
## Version: 0.6.1
## Date:    2021.07.16
## Description:    Menu entries for progmenu
## Updates:
##  - Added --ascii to help
##  - Added --ascii
##  - Updated -h
from ProgMenu.progmenu import EntryFlag, EntryArg

def filterFunc(f):
	'''Filter what to print.
Split args with semi-colon.'''
	return f.split(';')
def helpFunc():
	print('''    indusiatus.py -a <host device> [-cdfhloprst]
Network interface net to capture traffic.
  -a; --host;        Network interface to watch
  -c; --ascii;       Convert hex values to ASCII chars when applicable
  -d; --dump;        Dump raw packets.
                     Absolutely no processing the data will occur here
  -f; --filter=<sTv>; Filter print results.
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
                          - M: Source MAC address
                          - N: Destination MAC address
                          - P: Source port
                          - Q: Destination port
                          - S: IP source
                        <v>: Value, such as the IP, data length, etc...
  -h; --help;         Prints this page
  -l; --layer=<l>;    Determines number of layers to output, where 0 is all
                      Must be used in conjunction with --output
  -o; --output=<file>; Writes output to <file>.
                      Must use with --layer.
                      Overwrites existing files
  -p; --pretty;       Formatted printing
  -r; --raw;          Print the raw packet bytes
  -s; --short;        Pretty prints frames in one line
  -t; --frame=<type>; Frame type
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
EntryFlag("ascii", ['c', "ascii"], lambda:True, default=False)
EntryFlag("dump", ['d', "dump"], lambda:True)
EntryArg("filter", ['f', "filter"], filterFunc)
EntryFlag("help", ['h', "help"], helpFunc)
#EntryFlag("ip", ['i', "ip"], lambda:True, default=False)
EntryArg("layer", ['l', "layer"], lambda l:int(l), default=0)
EntryArg("output", ['o', "output"], outputFunc, recurse=["layer"])
EntryFlag("pretty", ['p', "pretty", "formatted"], lambda:True)
EntryFlag("raw", ['r', "raw"], lambda:True, default=False)
EntryFlag("short", ['s', "short"], lambda:True)
EntryArg("frame", ['t', "frame"], lambda t:t, default="ETH")

# Indusiatus
> Raw sockets catching traffic like a net

---

## Usage
Most common command is:
```
$ sudo ./indusiatus.py -a "wlan0" -pr
```
Make sure you replace "wlan0" with the device you want to capture on!

## Info
> Filter names, and other data that might be somewhat obscure

### News:
- RTAP was a PAIN to figure out so it currently only displays the RTAP header.

### Flags:
> Explanation of each flag in detail

- -d; --dump;
Dumps raw unprocessed packets to screen.
No processing is done here.
It's mostly just to test connectivity.

- -f; --filter=<sTv>;
Filters captured traffic.
Follows a specific syntax: <symbol type value>, where:
symbol is a specific symbol that represents the filter comparison; type is the type of data to check against; value is the user-passed value to compare. See below for list of symbols and types.
See [Filter Arguments](#filter-arguments) for a list of all symbols and types.

- -h; --help;
Just prints the help screen.
There's a decent amount of detail there.
ProgMenu detects when a help flag has been passed and will only print the help menu regardless of what other flags are called.
The normal program won't run when the help flag is called.

- -l; --layer=<layer>;
Determines the number of layers to write to file output.
Only used with --output.
Layer 0 is the entire frame, layer 1 is the whole frame minus the ETH header, layer 2 is the whole frame minus the packet header, etc...
Essentially, what will be written is everything from layer `<layer>` on, inclusive.
If a defined layer number is higher than the current frame's number of headers, a verbose error will be thrown and the frame will be ignored.

- -o; --output=<file>;
Writes raw bytes to <file>.
The raw bytes are prepended by 4 bytes: `0x3b0x##0x##0x3b`.
These bytes signify the size of the entire frame.
I surrounded the size with `0x3b` (hex for ';') just to hopefully make it slightly easier to distinguish my headers from the frame data.

- -p; --pretty;
Pretty prints the frame.
Recognizes the headers (as defined by --frame) and prints what I've deemed as the most relevant data in the frame.
This data is normally source and destination addresses, lengths, etc...
Each header is colour coded as determined by the file their class exists in (Frames=Purple, Packets=Dark Blue, etc...).
These colours are consistent with --raw.
--pretty can be run with --raw
--pretty is superceded by --short.

- -r; --raw;
Prints the raw packet.
Prints 16 bytes per line, with each line split into 2x8 bytes.
Starts each line with the byte count in hex.
The colours are consistent with --pretty.
Each colour identifies the entire header+and of that header's content.
The colour scheme is most obvious when using -p and -r together.
--raw can be run with --pretty.
--raw is superceded by --short.

- -s; --short;
Prints only the header names in their respective colours as defined by the files the classes live in.
Prints everything in one line per frame
Each line is preceded with the date/time of capture, and the captured packet count.

- -t; --frame=<type>;
Defines the type of frame Indusiatus is expecting.
This affects how Indusiatus parses through the data.
By passing the wrong frame type, displayed data will be incorrect.
Valid arguments for this flag are the same as the __Frame__ names under [Layer Names](#layer-names).

### Layer Names:
> These will all be capitalized

__Frame:__
- ETH: Ethernet Frame
- RTAP: 802.11 RadioTap Frame
__Packet:__
- IP: IPv4
- IPV6: IPv6
- ARP: Address Resolution Protocol
__IPv6 Extended Headers:__
- HBH
__Segment:__
- TCP: Transport Control Protocol
- UDP: User Datagram Protocol
- ICMP: Internet Control Message Protocol
- IGMP: Internet Group Management Protocol
__Payload:__
- GENERIC: Generic payload data; Unidentified (by me lol)

### Filter Arguments:
> List of all symbols and types, and a short description of each

__Symbols:__
- `'!': Not Equal`.
Ignores any frame that matches _type_ and _value_.

- `'=': Equal To`.
Matches any frame that agrees with _type_ and _value_.

- `'>': Greater Than`.
Matches any frame that's _type_ is greater than _value_.
Only works with 'L' _type_.

- `'<': Less Than`.
Matches any frame that's _type_ is less than _value_.
Only works with 'L' _type_.

__Types:__
- `'A': Data`.
Compares to entire packet.
This means that the user must pass bytes as _value_ as the entire frame will 99.9% of the time not be ASCII.

- `'D': Destination IP`.
Compares to destination IP.
This IP is found under the assumed packet layer, layer 1.

- `'H': Header Name`.
Compares to any header's name.
These names are found by iterating through the entire bundle chain until _value_ is found.
If there are 2 instances of the same header (which to my knowledge is rare, if not non-existent), but you are only filtering for one, you will need to use multiple filters.

- `'L': Data Length`.
Compares to the full length of the frame.

- `'S': Source IP`.
Compares to the source IP.
This IP is found in

---

## Terminology
> There are some terms I might interchange.
> This is here just to clarify any ambiguity

- __Bundle (Bundle Chain):__ In the code I refer to the fully parsed data as a "bundle". This is a tuple of headers, where each header refers to the next through the `upper` object variable.

- __Layers:__ When I say layers, I am almost always referring to the specific header in the bundle. I am __NOT__ referring to the TCP/IP model layers. Sometimes this extends to the header + all data above it. Layer 0 is the entire frame, layer 1 is from the packet up, etc...

---

## Bugs
### General
- IPv6 has so far been crashing the program. I know where the issue is, but I'm not able to simulate any IPv6 packets, not even a simple ping. This is a me issue if you know how please let me know!
- Specifying the wrong frame with --frame may crash the program.

### RTAP
- Because of the way stupid Radiotap headers are padded, changing the colour of RTAPPackets won't do anything. I've printed the whole RTAP header in raw using the RADIOFrame class' colours and length.
- RTAP type is still new here, so it is (less than) bare-bones, but shouldn't crash from legitimate traffic.
- Filters other than `L` don't work on RTAP. I need to update all RTAP data classes to fix this, but this is planned to be updated next!
- When outputting RTAP to a file, if `--layer` is specified layer 1-3 will exclude the entire Radiotap header. This is due to the way I implemented RTAPPackets, where each `it_present` dword counts as a layer. The easiest way to remember this is to count the layers when pretty printing!

---

## Notes For Me
- Radiotap has the dumbest formatting I've ever encountered! The padding is useless if every field's length is already known! What's the point of padding?!?!?!
- Need to change RADIOFrame to parse just the first 4 bytes and the present dwords. Need to implement a pointer system where we check the length of the current field and if the pointer is "unaligned" then assume the next n bytes are padding until we reach an alignment.
- I want to add port filters!
- With all these new filters I might need to start relying less on specific layers to check (ex. check IPs on layer 2). So far there shouldn't be an issue with this, but with the development of RTAP it might be beneficial to make the filter parsing more dynamic.

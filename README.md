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
### Layer names:
> These will all be capitalized

__Frame:__
- ETH: Ethernet Frame
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

---

## Bugs
- IPv6 has so far been crashing the program. I know where the issue is, but I'm not able to simulate any IPv6 packets, not even a simple ping. This is a me issue if you know how please let me know!

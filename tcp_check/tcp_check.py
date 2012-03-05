#!/usr/bin/python
# check_mk script to check TCP connections to a remote host.
# first written to simply check transit down a leased line

from socket import *

checks = [
    ['11.22.33.44', 8443],
    ['12.13.14.15', 6000],
]

setdefaulttimeout(5)
count=0
for ip,port in checks:
    s = socket(AF_INET, SOCK_STREAM)
    result = s.connect_ex((ip,port))
    if ( 0 == result ):
        print "0 Leased_Line_Test_" + str(count) + " - OK: %s:%d Reachable" % (ip,port)
    else:
        print "2 Leased_Line_Test_" + str(count) + " - CRITICAL: %s:%d Not Reachable" % (ip,port)
    s.close()
    count=count+1

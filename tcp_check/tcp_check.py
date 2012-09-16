#!/usr/bin/env python
# check_mk script to check TCP connections to a remote host.
# first written to simply check transit down a leased line
# Herward Cooper <coops@fawk.eu> - 2011

from socket import *

# Out list of checks, in the form: ['ip', port]
checks = [
        ['11.22.33.44', 8443],
        ['12.13.14.15', 6000],
        ['127.0.0.1', 80],
]

# What to prefix all the check names with
prefix = "TCP_Check_"

# How long to wait for each check?
timeout = 5

setdefaulttimeout(timeout)

for ip,port in checks:

    # Define a new socket
    s = socket(AF_INET, SOCK_STREAM)

    # Form the check name
    chkname = prefix + ip + ":" + str(port)

    # Open the connection
    result = s.connect_ex((ip,port))

    # Report the result
    if ( result == 0 ):
        print "0 %s - OK - %s:%d Reachable" % (chkname,ip,port)
    else:
        print "2 %s - CRITICAL - %s:%d Unreachable" % (chkname,ip,port)

    # Close the connection
    s.close()

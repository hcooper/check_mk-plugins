#!/usr/bin/python

# A check_mk plugin to monitor the status of an HAProxy server.
# Hereward Cooper <coops@fawk.eu>

# Requirements:
# - HAproxy socket
#   (config: "stats socket /var/run/haproxy.socket")

import os
import re
import sys
from cStringIO import StringIO
import socket
from time import time

__version__ = "0.2"
__author__ = "Hereward Cooper <coops@fawk.eu>"
__website__ = "http://github.com/hcooper/haproxy-tools/"


def build_array(rawstats):
    """ Convert the raw stats into nested arrays. Much nicer to use.
    This functions creates an array, with each element being a dictonary of checks for each server
    e.g. servers = [ {pxname: app1, rate: 15...}, {pxname: app2, rate: 7...} ] """

    stats=[]

    for line in rawstats.split('\n'):

        if re.match(r'^\s*$', line):  # skip empty lines
            continue

        values = line.split(',')

        if re.match(r'^#', line):  # first line contains the header names
            titles = values
            titles[0] = titles[0][2:]  # remove the '# ' from the first element
            continue

        stats.append(dict(zip(titles,values)))  # create the dict containing our results

    return stats


def run_checks(servers):
    """ Interate through each server, and then each defined check, and compare the values to
    the critical/warning levels, then alert if need be. """

    for server in servers:
        server['fullname'] = server['pxname'] + "/" + server['svname']  # Combine 'svname' and 'pxname' to get a unique name

        # Define some variables before use
        result=""           # The complete set of results for each server's checks
        allperf=""          # The complete set of all performance data for a server
        alert_warn=False    # Flag set if  check makes a server WARN
        alert_crit=False    #   "   "   "   "   "   "   "   "   CRIT

        for check,warn,crit in checks:
            output=""
            perfdata=""

            # If the value we're looking for isn't present, skip it. (e.g. FRONTEND doesn't have chkfail)
            if not server[check]:
                continue

            # Special check for the "status" field as it's not a numeric value
            if check == "status":
                if server['status'] == "UP":
                    output += "status UP"
                elif server['status'] == "DOWN":
                    output += "status DOWN"
                    alert_crit = True
                elif server['status'] == "OPEN":
                    output += "status OPEN"
                # Add more status options here
    
            # Generic check for the other fields which are numeric
            # Make sure int() is used when needed!
            else:
                if int(server[check]) >= int(warn) and int(server[check]) < int(crit):
                    output += check + " WARN " + server[check] + ", "
                    alert_warn = True
                if int(server[check]) >= int(crit):
                    output += check + " CRIT " + server[check] + ", "
                    alert_crit = True
                #if server[check] < warn:          # Disabled so OK doesn't give out stats 
                    #output += "| " + check + " OK " + server[check]

                perfdata += check + "=" + server[check] + ";" + warn + ";" + crit

            # Build the output performance data, putting | in the right places
            if allperf == "":
                allperf = perfdata
            elif perfdata != "":
                allperf += "|" + perfdata

            # Build the check output
            result += output

        # If any of our checks have set the crit/warn flags, act on it
        if alert_crit:
            print "2 HAProxy_%s %s CRITICAL - [%s]" % (server['fullname'], allperf, result)
        elif alert_warn:
            print "1 HAProxy_%s %s WARNING - [%s]" % (server['fullname'], allperf, result)
        else:
            print "0 HAProxy_%s %s OK - [%s]" % (server['fullname'], allperf, result)


class HAProxyStats(object):
    """ Used for communicating with HAProxy through its local UNIX socket interface"""

    def __init__(self, socket_name=None):
        self.socket_name = socket_name

    def getstats(self, timeout=200):
        """ Executes a HAProxy command by sending a message to a HAProxy's local
        UNIX socket and waiting up to 'timeout' milliseconds for the response """

        buff = StringIO()
        end = time() + timeout

        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        try:
            client.connect(self.socket_name)
            client.send('show stat' + '\n')

            while time() <=  end:
                data = client.recv(4096)
                if data:
                    buff.write(data)
                else:
                    return build_array(buff.getvalue())
        except:
            print "Failed to retrieve stats"
            sys.exit(1)
        finally:
            client.close()



if __name__ == "__main__":

    socketfile = "/var/run/haproxy.socket"

    if not os.path.exists(socketfile):
            print "Socket does not exist"
            sys.exit(1)

    statssocket = HAProxyStats(socketfile)
    stats = statssocket.getstats()

    from haproxychecks import checks

    run_checks(stats)

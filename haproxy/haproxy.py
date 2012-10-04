#!/usr/bin/python

# A check_mk plugin to monitor the status of an HAProxy server.
# Hereward Cooper <coops@fawk.eu>

# Requirements:
# - Netcat (nc command)
# - HAproxy socket
#   (config: "stats socket /var/run/haproxy.socket")

# Precaution: check_mk presumes each check is a unique name. However HAProxy allows
# servers to be called the same. If this happens, checks will overwrite each other.

import os
import re
import sys

__version__ = "0.1"
__author__ = "Hereward Cooper <coops@fawk.eu>"
__website__ = "http://github.com/hcooper/haproxy-tools/"


def build_array():

    """
    Convert the raw stats into nested arrays. Much nicer to use.
    This functions creates an array, with each element being a dictonary of checks for each server
    e.g. servers = [ {pxname: app1, rate: 15...}, {pxname: app2, rate: 7...} ]
    """

    data = os.popen(command).read()     # Retrieve the raw data

    #Initalize our array
    global servers
    servers=[]

    for line in data.split('\n'):		# split out each line of raw input
        if re.match(r'^\s*$', line):    # skip empty lines
            continue
        i=0
        dict={}
        for var in line.split(','):         # for each value put it in a dictonary matching the human readable name in "title_array"
                dict[title_array[i]]=var
                i=i+1
        servers.append(dict)

    return servers


def run_checks():

    """
    Interate through each server, and then each defined check, and compare the values to
    the critical/warning levels, then alert if need be.
    """

    for server in servers:
        if server['svname'] == "FRONTEND" or server['svname'] == "BACKEND":
            server['svname'] = server['svname'] + "_" + server['pxname']

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
                elif server['status'] == 
    
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
            print "2 HAProxy_%s %s CRITICAL - [%s]" % (server['svname'], allperf, result)
        elif alert_warn:
            print "1 HAProxy_%s %s WARNING - [%s]" % (server['svname'], allperf, result)
        else:
            print "0 HAProxy_%s %s OK - [%s]" % (server['svname'], allperf, result)

if __name__ == "__main__":

    # Location of the HAProxy socket
    socket="/var/run/haproxy.socket"

    # A list of servers to ignore from the CSV output (format: "|^name")
    ignore="^haproxystats"

    # This is the command to run to retrieve the raw stats from the socket
    command="echo 'show stat' | nc -U %s | egrep -v '(^#|%s)'"%(socket,ignore)

    # These are the names haproxy calls each of the columns it outputs. We can improve the names
    # by just changing them here. But most of them are fine
    titles="pxname,svname,qcur,qmax,scur,smax,slim,stot,bin,bout,dreq,dresp,ereq,econ,eresp,\
        wretr,wredis,status,weight,act,bck,chkfail,chkdown,lastchg,downtime,qlimit,\
        pid,iid,sid,throttle,lbtot,tracked,type,rate,rate_lim,rate_max,check_status,\
        check_code,check_duration,hrsp_1xx,hrsp_2xx,hrsp_3xx,hrsp_4xx,hrsp_5xx,\
        hrsp_other,hanafail,req_rate,req_rate_max,req_tot,cli_abrt,srv_abrt,misc"

    # Put the column titles into an array
    title_array=titles.split(',')

    # Read in our list of checks
    from checks import checks

    build_array()
    run_checks()

#!/usr/bin/python

# This is a local plugin for check_mk, suitable for monitoring
# any service variables which are presented in a list. Currently
# sucessfully tested with MySQL and Varnish.

# Hereward Cooper <coops@fawk.eu>

#------------------------------------------------------------
# CONFIGURATION
#------------------------------------------------------------

# What's the command to run to get our raw data?
#status_command="/usr/bin/varnishstat -1"
status_command="mysql -e 'show status'"
#status_command="mysqladmin status | sed 's/  /\\n/g' | sed 's/ /_/g' | sed 's/:_/ /g'"


# What's a human-friendly prefix to name our checks?
#prefix = "Varnish_"
prefix = "MySQL_"

# What variables shall we actually check for? Format:
# ("variable name", warning threshold, critical threshold)
checks = [
#   ( "Queries_per_second_avg", 1, 5),
   ( "Slow_queries", 1, 5),
]

#------------------------------------------------------------
# PREPARE FOR BATTLE
#------------------------------------------------------------

import sys
import os

# Run the command to retrieve the raw data
status = os.popen(status_command).read()


#------------------------------------------------------------
# DEBUG
#------------------------------------------------------------

# To save commenting and uncommenting each time, just call this debug function
def debug():
        print "-----------------------"
        print "DEBUG: Parsed Variables"
        print "-----------------------"
        for line in status.split('\n'):
                try:
                        sys.stdout.write("VAR: " + line.split()[0])
                except:
                        continue
                try:
                    print " - " + line.split()[1]
                except:
                    continue

        print "----------------"
        print "DEBUG: My Checks"
        print "----------------"
        for check,warn,crit in checks:
            print check, warn, crit

#------------------------------------------------------------
# THE MAGIC
#------------------------------------------------------------

# Function to output the check result in check_mk format
def output(type, check, value):
    print str(type) + " " + prefix + check + " - " + str(value)

# Read through each line in the output of SHOW STATUS
def run_checks():
        for line in status.splitlines():
            # Sometimes we have a mare reading the first and last lines. Skip if needed.
                try:
                    var = line.split()[0]
                except:
                    continue
        
                # Some variables don't actually have a value set. Handle this (skip for now).
                try:
                    var_value = float(line.split()[1])
                except:
                    continue
        
                # Read through each of our configured variables to check
                for check,warn,crit in checks:
                    # Is the variable one on the list to check?
                    if var == check:
                        if var_value > crit:
                            output(2,var,"CRITICAL: " + prefix + var + " " + str(var_value))
                        elif var_value > warn:
                            output(1,var,"WARNING: " + prefix + var + " " + str(var_value))
                        else:
                            output(0,var,"OK: " + prefix + var + " " + str(var_value))

# Actually do some work!
run_checks()
#debug()

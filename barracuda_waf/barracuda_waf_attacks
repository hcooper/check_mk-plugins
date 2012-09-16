#!/usr/bin/env python

# Monitor the number of attacks a Barracuda WAF is fighting off.
# Herward Cooper <coops@fawk.eu> - 2012

# OID .1.3.6.1.4.1.20632.8 is meant to return the number of attacks in the last hour.
# However due to a bug (or wrong documentation) it actually returns the total number
# of attacks. We therefore use check_mk's internal 'get_counter' function to track this
# value, and turn it into a rate which we can monitor.

barracuda_waf_attacks_default_values = (3, 20)

def inventory_barracuda_waf_attacks(checkname, info):
    inventory=[]
    status = int(info[0][0])
    inventory.append( (None, None, "barracuda_waf_attacks_default_values") )
    return inventory


def check_barracuda_waf_attacks(item, params, info):
    this_time = float(time.time())
    state = int(info[0][0])
    attacks_timedif, attacks_rate = get_counter("barracuda_waf_attacks", this_time, state)
    warn, crit = params
    perfdata = [ ( "attacks", attacks_rate, warn, crit ) ]
    if attacks_rate > crit:
        return (2, "CRITICAL - %s attacks per second" % attacks_rate, perfdata)
    elif attacks_rate > warn:
        return (1, "WARNING - %s attacks per second" % attacks_rate, perfdata)
    else:
        return (0, "OK - %s attacks per second" % attacks_rate, perfdata)

check_info["barracuda_waf_attacks"] = (check_barracuda_waf_attacks, "Barracuda WAF Attacks", 1, inventory_barracuda_waf_attacks)

snmp_info["barracuda_waf_attacks"] = ( ".1.3.6.1.4.1.20632.8", ["4"] )
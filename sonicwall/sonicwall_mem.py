#!/usr/bin/env python

# Monitoring the Mem usage of a Sonicwall
# Herward Cooper <coops@fawk.eu> - 2012

# Uses OID 1.3.6.1.4.1.8741.1.3.1.4.0

sonicwall_mem_default_values = (35, 40)

def inventory_sonicwall_mem(checkname, info):
    inventory=[]
    inventory.append( (None, None, "sonicwall_mem_default_values") )
    return inventory


def check_sonicwall_mem(item, params, info):
    warn, crit = params
    state = int(info[0][0])
    perfdata = [ ( "cpu", state, warn, crit ) ]
    if state > crit:
        return (2, "CRITICAL - Mem is %s percent" % state, perfdata)
    elif state > warn:
        return (1, "WARNING - Mem is %s percent" % state, perfdata)
    else:
        return (0, "OK - Mem is %s percent" % state, perfdata)

check_info["sonicwall_mem"] = (check_sonicwall_mem, "Sonicwall Mem", 1, inventory_sonicwall_mem)

snmp_info["sonicwall_mem"] = ( ".1.3.6.1.4.1.8741.1.3.1.4", [ "0" ] )

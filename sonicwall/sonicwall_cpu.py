#!/usr/bin/env python

# Monitoring the CPU usage of a Sonicwall
# Herward Cooper <coops@fawk.eu> - 2012

# Uses OID .1.3.6.1.4.1.8741.1.3.1.3.0

sonicwall_cpu_default_values = (35, 40)

def inventory_sonicwall_cpu(checkname, info):
    inventory=[]
    inventory.append( (None, None, "sonicwall_cpu_default_values") )
    return inventory


def check_sonicwall_cpu(item, params, info):
    warn, crit = params
    state = int(info[0][0])
    perfdata = [ ( "cpu", state, warn, crit ) ]
    if state > crit:
        return (2, "CRITICAL - CPU is %s percent" % state, perfdata)
    elif state > warn:
        return (1, "WARNING - CPU is %s percent" % state, perfdata)
    else:
        return (0, "OK - CPU is %s percent" % state, perfdata)

check_info["sonicwall_cpu"] = (check_sonicwall_cpu, "Sonicwall CPU", 1, inventory_sonicwall_cpu)

snmp_info["sonicwall_cpu"] = ( ".1.3.6.1.4.1.8741.1.3.1.3", [ "0" ] )

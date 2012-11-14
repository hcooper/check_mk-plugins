#!/usr/bin/env python

# Monitoring the memory of a sonicwall
# Herward Cooper <coops@fawk.eu> - 2012

# Used OID 1.3.6.1.4.1.8741.1.3.1.4.0

def inventory_sonicwall_mem(checkname, info):
    inventory=[]
    status = int(info[0][0])
    if status < 11:
        inventory.append( (None, None) )
    return inventory


def check_sonicwall_mem(item, params, info):
    state = int(info[0][0])
    if state == 8:
        return (0, "OK - Peer is compatible")
    else:
        return (2, "CRITICAL - Peer is not compatible!")
    return (3, "UNKNOWN - unhandled problem")

check_info["sonicwall_mem"] = (check_sonicwall_mem, "Sonicwall Memory", 0, inventory_sonicwall_mem)

snmp_info["sonicwall_mem"] = ( "1.3.6.1.4.1.8741.1.3.1.4", [ "0" ] )

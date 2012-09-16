#!/usr/bin/env python

# Quick hack to monitoring LSI MegaRaid via SNMP with check_mk
# Tested using Windows LSI tools
# Hereward Cooper <coops@fawk.eu> - Sep 2012

# Currently checks 4 values, with a base OID of 1.3.6.1.4.1.3582.4.1.4.1.2.1
# .19 = vdDegradedCount
# .20 = vdOfflineCount
# .24 = pdDiskFailedCount
# .23 = pdDiskPredFailureCount

def inventory_lsi_megaraid(checkname, info):
    inventory = []
    inventory.append( (None, None) )
    return inventory


def check_lsi_megaraid(item, params, info):

    # The 'nice' names for our checks
    checks = ['vdDegradedCount', 'vdOfflineCount', 'pdDiskFailedCount', 'pdDiskPredFailureCount']

    # Make a dictonary of the check name and the result
    results = dict(zip(checks, info[0]))

    # Check the results and return appropriately
    for check in results:
        if results[check] == '0':
            continue
        else:
            return (2, "CRITICAL - %s: %s" % (check, results[check]))

    # If we haven't returned with an error so far, return OK now
    return (0, "OK - No reported errors")


check_info["lsi_megaraid"] = (check_lsi_megaraid, "LSI MegaRAID", 0, inventory_lsi_megaraid)
snmp_info["lsi_megaraid"] = ( ".1.3.6.1.4.1.3582.4.1.4.1.2.1", ["19", "20", "24", "23"] )
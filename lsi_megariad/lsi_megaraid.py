#!/usr/bin/python

# Quick hack to monitoring LSI MegaRaid via SNMP

def inventory_lsi_megaraid(checkname, info):
    inventory = []
    inventory.append( (None, None) )
    return inventory


def check_lsi_megaraid(item, params, info):

    # Take the results array, and split it into each of our attributes
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
    return (0, "OK - no reported errors")


check_info["lsi_megaraid"] = (check_lsi_megaraid, "LSI MegaRAID", 0, inventory_lsi_megaraid)
snmp_info["lsi_megaraid"] = ( ".1.3.6.1.4.1.3582.4.1.4.1.2.1", ["19", "20", "24", "23"] )
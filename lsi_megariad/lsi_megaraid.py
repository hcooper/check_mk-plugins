#!/usr/bin/python

# Quick hack to monitoring LSI MegaRaid via SNMP

def inventory_lsi_megaraid(checkname, info):
    inventory = []
    inventory.append( (None, None) )
    return inventory


def check_lsi_megaraid(item, params, info):

    # Take the results array, and split it into each of our attributes
    vdDegradedCount, vdOfflineCount, pdDiskFailedCount, pdDiskPredFailureCount = info[0]

    # Do the logic to determine if we should alert or not
    if vdDegradedCount != "0":
        return (2, "CRITICAL - vdDegradedCount > 0")
    elif vdOfflineCount != "0":
        retrun (2, "CRITICAL - vdOfflineCount > 0")
    elif pdDiskFailedCount != "0":
        return (2, "CRITICAL - pdDiskFailedCount > 0")
    elif pdDiskPredFailureCount != "0":
        return (2, "CRITICAL - pdDiskPredFailureCount > 0")
    else:
        return (0, "OK - no reported errors")


check_info["lsi_megaraid"] = (check_lsi_megaraid, "LSI MegaRAID", 0, inventory_lsi_megaraid)

snmp_info["lsi_megaraid"] = ( ".1.3.6.1.4.1.3582.4.1.4.1.2.1", ["19", "20", "24", "23"] )


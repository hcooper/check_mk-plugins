#!/bin/bash
#
# A mysql replication plugin for the check_mk nagios system.
# Place me in /usr/lib/check_mk_agent/local on the client
#
# Hereward Cooper <coops@iomart.com> - 16/06/11

MYSQL_USER="root"
MYSQL_PASS="Pa$$word"

# Anything below DELAY_OK is fine. Anything between
# DELAY_OK and DELAY_WARNING is a warning. Anything
# above DELAY_WARNING is critical.
DELAY_OK=600
DELAY_WARNING=3600


MYSQL_STATUS=`mysql -u$MYSQL_USER -p$MYSQL_PASS -e "SHOW SLAVE STATUS\G" | egrep 'Slave_.*_Running|Seconds_Behind_Master' | sed 's/^ *//'`

echo "$MYSQL_STATUS" | sed -n '1p' | grep -q Yes && IO=1 || IO=0
echo "$MYSQL_STATUS" | sed -n '2p' | grep -q Yes && SQL=1 || SQL=0
DELAY=`echo "$MYSQL_STATUS" | sed -n '3p' | cut -d " " -f 2`

## Check Slave_IO_Running status
if [ $IO = "1" ]; then
        echo "0 MySQL_Rep_IO - OK - Replication IO Running"
else
        echo "2 MySQL_Rep_IO - CRITICAL - Repication IO Stopped"
fi

## Check Slave_SQL_Running status
if [ $SQL = "1" ]; then
        echo "0 MySQL_Rep_SQL - OK - Replication SQL Running"
else
        echo "2 MySQL_Rep_SQL - CRITICAL - Replication SQL Stopped"
fi

## Check Seconds_Behind_Master value
if [ $DELAY = "NULL" ]; then
        echo "2 MySQL_Rep_Delay - CRITICAL - Replication delay NULL"
elif [ $DELAY -lt $DELAY_OK ]; then
        echo "0 MySQL_Rep_Delay - OK - Replication delay $DELAY seconds"
elif [ $DELAY -lt $DELAY_WARNING ]; then
        echo "1 MySQL_Rep_Delay - WARNING - Replication delay $DELAY seconds"
elif [ $DELAY -ge $DELAY_WARNING ]; then
        echo "2 MySQL_Rep_Delay - CRITICAL - Replication delay $DELAY seconds"
fi


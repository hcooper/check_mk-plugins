#!/bin/bash

# A mysql replication plugin for the check_mk nagios system.
# Place me in /usr/lib/check_mk_agent/local on the client
# Hereward Cooper <coops@fawk.eu> - 16/06/11

MYSQL_USER="user"
MYSQL_PASS="Pa$$word"

# Anything below DELAY_WARNING is fine. Anything between
# DELAY_WARNING and DELAY_CRITICAL is throw up a warning. Anything
# above DELAY_CRITICAL will trigger a critical alert.
DELAY_WARNING=60
DELAY_CRITICAL=360

# Graph details
MIN=0
MAX=400


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
        echo "2 MySQL_Rep_Delay delay=$DELAY;$DELAY_WARNING;$DELAY_CRITICAL;$MIN;$MAX CRITICAL - Replication delay NULL"
elif [ $DELAY -lt $DELAY_WARNING ]; then
        echo "0 MySQL_Rep_Delay delay=$DELAY;$DELAY_WARNING;$DELAY_CRITICAL;$MIN;$MAX OK - Replication delay $DELAY seconds"
elif [ $DELAY -lt $DELAY_CRITICAL ]; then
        echo "1 MySQL_Rep_Delay delay=$DELAY;$DELAY_WARNING;$DELAY_CRITICAL;$MIN;$MAX WARNING - Replication delay $DELAY seconds"
elif [ $DELAY -ge $DELAY_CRITICAL ]; then
        echo "2 MySQL_Rep_Delay delay=$DELAY;$DELAY_WARNING;$DELAY_CRITICAL;$MIN;$MAX CRITICAL - Replication delay $DELAY seconds"
fi

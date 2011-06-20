# generic_local check_mk plugin

## Overview
The generic_local plugin for check_mk provides an easy way to monitor the status
of a service without having to script a custom plugin from scratch.

Originally started to monitoring any given values reported my "SHOW STATUS" in
MySQL, is was updated to be genericified to allow monitoring of any service
which can present it's stats in a two column format.

## Installation
The plugin is designed to be a *local* plugin, which doesn't require any
configuration on the server side. This means changes to thresholds are done
locally too.

Just place the script (set as executable) in the check_mk_agent local directory
(/usr/lib/check_mk_agent/local on Debian).

## Example Configurations
### Varnish

```
status_command="/usr/bin/varnishstat -1"
prefix = "Varnish_"
checks = [
       ( "backend_fail", 10, 100),
       ( "client_conn", 40, 100)
]
```

Example output:
```
2 Varnish_client_conn - CRITICAL: Varnish_client_conn 4630
1 Varnish_backend_fail - WARNING: Varnish_backend_fail 18
```

### MySQL

```
status_command="/usr/bin/mysql -e 'SHOW STATUS'"
prefix = "MySQL_"
checks = [
        ( "Qcache_lowmem_prunes", 10, 100),
        ( "Max_used_connections", 25, 30),
        ( "Threads_connected", 5, 10),
        ( "Open_files", 512, 1024),
        ( "Open_tables", 256, 512),
        ( "Slow_queries", 10, 100)
]
```

Example output:
```
0 MySQL_Max_used_connections - OK: MySQL_Max_used_connections 20
0 MySQL_Open_files - OK: MySQL_Open_files 445
0 MySQL_Open_tables - OK: MySQL_Open_tables 256
0 MySQL_Qcache_lowmem_prunes - OK: MySQL_Qcache_lowmem_prunes 0
0 MySQL_Slow_queries - OK: MySQL_Slow_queries 0
0 MySQL_Threads_connected - OK: MySQL_Threads_connected 1
```

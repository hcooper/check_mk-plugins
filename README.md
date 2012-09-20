A bunch of check_mk plugins
===========================
Just read the scripts, the comments explain most things.

There is a mix of two types of checks. Firstly 'local' checks, which are run on the
client-side just by placing in the correct directory (e.g. /usr/lib/check_mk_agent/local).
Secondarily there are server-side checks which automatically find the service to monitor
(mostly by looking for a specific SNMP OID).

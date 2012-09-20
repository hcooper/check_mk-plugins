A bunch of check_mk plugins
===========================
Just read the scripts, the comments explain most things.

SNMP checks
-----------
These are installed on the check_mk server, (e.g. /usr/share/check_mk/checks), and if the
specific SNMP OID for that check returns a result it will be added to the inventory. I've had
to write these mainly for proprietary piece of equipment (physical firewalls, raid cards etc).
**Note:** remove the file extension when placing them in the 'checks' directory.

Local checks
------------
These are installed on the client server, (e.g. /usr/lib/check_mk_agent/local). They have
no server-side part, and handle all the logic needed to perform the check themselves.

#!/usr/bin/env python3

'''
Check there's recent good backups for each host in backuppc.
Requires:
  backuppc's cli tools (BackupPC_serverMesg)
  python's shutil module
  hash-to-json script.pl (in this repo, installed at /usr/local/bin)
'''

import json
import sh
import time

# Thresholds, in hours.
WARN = 36
CRIT = 72

now = time.time()

# Use backuppc's cli tools to get the data we want, then convert the perl hash output
# into json. It's pretty hacky.
srv_msg=sh.Command('/usr/share/backuppc/bin/BackupPC_serverMesg')
hash_to_json=sh.Command('/usr/local/bin/hash-to-json.pl')
j=json.loads(hash_to_json(sh.sed(srv_msg('status hosts'),'s/Got reply: //')).stdout)

for host, info in j.items():
    # Skip backuppc's housekeeping jobs.
    if host in (' admin ', ' admin1 ', ' trashClean '):
        continue

    d = now - info["lastGoodBackupTime"]
    d_nice = round(d/60/60, 2)

    if d < (60*60*WARN):
        print(
            f"0 {host}_backup_age - OK {host}'s last good backup is {d_nice}h old."
        )
    elif (60*60*WARN) < d < (60*60*CRIT):
        print(
            f"1 {host}_backup_age - WARNING {host}'s last good backup is {d_nice}h old."
        )
    else:
        print(
            f"2 {host}_backup_age - CRITICAL {host}'s last good backup is {d_nice}h old."
        )

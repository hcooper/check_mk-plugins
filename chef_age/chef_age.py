#!/usr/bin/env python3

''' Check the age of a status file chef touches '''

import os
import time

# Thresholds, in hours.
WARN = 3
CRIT = 24

try:
    s = os.stat('/run/chef.last_success')
    d = time.time() - s.st_mtime
    d_nice = round(d/60/60, 2)

    if d < (60*60*WARN):
        print(f"0 chef_success_age - OK chef successfully ran {d_nice} hours ago.")
    elif (60*60*WARN) < d < (60*60*CRIT):
        print(f"1 chef_success_age - WARNING chef hasn't run successfully for {d_nice} hours.")
    else:
        print(f"2 chef_success_age - CRITICAL chef hasn't run successfully for {d_nice} hours.")
except:
    print(f"3 chef_success_age - UNKNOWN failure in calculating chef age.")
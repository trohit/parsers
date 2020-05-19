#!/usr/local/bin/python3.7
"""
tool to show deltas in timestamps between successive journalctl  logs
eg.
timeline.txt
0:00:00 start op
0:00:59.008183 end op
0:28:58.646555 phase completed
Usage:
    cat timeline.txt | ./delta.py

Sample O/p:
0:00:00 start op
0:00:59.008183 end op
0:28:58.646555 phase completed

"""

import datetime
import sys
def get_dt(line):
    il = line[:22]
    dt = datetime.datetime.strptime(il, "%b %d %H:%M:%S.%f")
    #print(dt)
    return dt
#main
is_ts_inited = False
t2 = t1 = ''
if len(sys.argv) == 2:
    fh = open(sys.argv[1])
else:
    fh = sys.stdin

while True:
    line = fh.readline()
    if not line:
        break
    #print(line)
    if not is_ts_inited:
        #print("1st time")
        t2 = t1 = get_dt(line)
        is_ts_inited = True
    else:
        t1 = t2
        t2 = get_dt(line)
    #print("t2:"+str(t2))
    #print("t1:"+str(t1))
    print(str(t2 - t1) + line[22:].rstrip())
fh.close()

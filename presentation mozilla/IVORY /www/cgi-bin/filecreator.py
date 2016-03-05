#!/usr/bin/python

import os

os.popen("hadoop dfsadmin -report |grep 192.168.5|cut -f 2 -d \" \"|cut -f 1 -d \":\">datanode.txt").read()
os.popen("hadoop dfsadmin -report| head -11|tail -1|cut -f 3 -d \" \">numdata.txt").read()
os.popen("hadoop job -list-active-trackers | wc -l>numtask.txt").read()



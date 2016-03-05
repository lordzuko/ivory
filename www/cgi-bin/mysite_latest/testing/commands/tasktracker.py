#!/usr/bin/python2

import os
import sys
import commands as cmd

def main(argv):
  
  if len(argv) == 4:
    sys.exit("./tasktracker.py <namenode_ip> <jobtracker_ip> ")
  
  #changes made in /etc/hadoop/mapred-site.xml
  os.popen("./mapred-site_modifier.py T "+ argv[1]+" n")
  
  #changes made in /etc/hadoop/core-site.xml
  os.popen("./core-site_modifier.py "+argv[0]+" n")
  
  os.popen("hadoop-daemon.sh start tasktracker")
  status,output = cmd.getstatusoutput("/usr/java/jdk1.7.0_51/bin/jps | grep TaskTracker | awk -F' ' '{print$2}'")
  
  if output == 'TaskTracker':
    pass
  else:
    sys.exit("TaskTracker not started!!")

if __name__=='__main__':
  main(sys.argv[1:])

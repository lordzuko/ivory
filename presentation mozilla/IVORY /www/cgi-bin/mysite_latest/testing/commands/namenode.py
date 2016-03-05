#!/usr/bin/python2

import os
import sys
import commands as cmd

def main(argv):
  
  if len(argv) == 4:
    sys.exit("./namenode <namenode_ip> <enable_trash(y/n)> <rep_factor> <blk_size>")
  
  #changes made in /etc/hadoop/hdfs-site.xml 
  os.popen("./core-site_modifier.py "+argv[0]+" "+argv[1])
  #changes made in /etc/hadoop/core-site.xml
  os.popen("./hdfs-site_modifier.py N n "+argv[2]+" "+argv[3])
  
  os.popen("hadoop-daemon.sh start namenode")
  status,output = cmd.getstatusoutput("/usr/java/jdk1.7.0_51/bin/jps | grep NameNode | awk -F' ' '{print$2}'")
  
  if output == 'NameNode':
    sys.exit(0)
  else:
    sys.exit(1)

if __name__=='__main__':
  main(sys.argv[1:])

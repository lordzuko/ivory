#!/usr/bin/python2

import os 
import sys
import commands as cmd


# namenode_ip ,enable_trash

def main(argv):
  
  if len(argv) != 2:
    sys.exit("Usage ./core-site_modifier.py <namenode_ip> <enable_trash(y/n)>")
  
  if not os.system("rpm -q hadoop"):
    os.popen("yum install hadoop")
  
  os.popen("sed -i 's/<\/configuration>/./' hadoop/core-site.xml")
    
  _file = open("hadoop/core-site.xml","a")
  
  s = '''
         <property>
         <name>hdfs.default.name</name>
         <value>hdfs://%s:9001</value>
         </property>
      '''
  r = '%s\n' %(str(argv[0]))

  _file.write(r)

  """ ------------------Enable Trash--------------------------"""
  if argv[1] =='n':
    pass
  else
    s = '''
            <property>
            <name>fs.trash.interval</name>
            <value>10</value>
            </property>
          '''
  
    _file.write(s)
  """---------------------------------------------------------"""
  
  _file.write("</configuration>")
  _file.close()
  
if __name__ == '__main__':
  main(sys.argv[1:])

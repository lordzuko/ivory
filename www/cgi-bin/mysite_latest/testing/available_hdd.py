#!/usr/bin/python2

import os 
import sys

from sys import argv

def main(argv):
  
  if len(argv) != 1:
    sys.exit("Usage ./available_hdd hostip")
  
  """-----------------------checking available disk on hdd & ram-------------------------"""

  #total size available on disk  
  total_size = os.popen("parted /dev/sda print | grep Disk | awk -F ' ' '{print $3}' | awk -F 'G' '{print $1}'").read()

  #total used space on disk 
  used_space = os.popen("parted /dev/sda print | tail -2  | awk -F ' ' '{print $3}' | awk -F 'G' '{print $1}'").read()

  #calculating available disk space
  available_space = int(total_size) - int(used_space) 
 
  #this command parses ip out of ifconfig 
  ip = os.popen("ifconfig | grep 192.168.0 | awk -F' ' '{print $2}' | awk -F':' '{print $2}'").read()

  #total size of ram 
  available_ram = os.popen("free -tm | grep Mem | awk -F' ' '{print $4}'").read()


  file_entry = "%r %r %r" % (ip.strip('\n'),available_space,available_ram.strip('\n'))
  print file_entry

  #printing 'ip available_space' to memspace file
  s = ("mkdir /hadoop_setup; touch /hadoop_setup/%s") %(ip.strip('\n'))
  os.popen(s) 
  s = "echo %s > /hadoop_setup/%s" % (ip.strip('\n'),file_entry)
  os.popen(s)

  #scp the file to host i.e. httpd server
  temp = 'sshpass -p "redhat" scp  -r -o StrictHostKeyChecking=no /hadoop_setup/%s root@'+argv[0]+':/root/Desktop/testing/temp/" > /dev/null 2>&1 &' %(ip.strip('\n'))
  #temp = "scp /hadoop_setup/"+ip.strip('\n')+" "+argv[0]+":/root/Desktop/testing/temp/"
  os.popen(temp)

  """------------------------------------------------------------------------------------"""
  

if __name__ == '__main__':
  main(sys.argv[1:])


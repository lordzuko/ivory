#!/usr/bin/python2

import thread
import os 
import sys
import commands as cmd
import cgi
import cgitb
cgitb.enable()


print 'Content-type: text/html'
print '\n'

form = cgi.FieldStorage()

blk_size = 'n'
replication = 'n'
heartBeat = 'n'
chk_point = 'n'
scheduler = "FAIR"
minHeap = 'n'
maxHeap = 'n'


print "<h1>10%</h1>"
"setting up namenode"
namenode_ip = '127.0.0.1'
s = ('namenode.py %s y %s %s > /dev/null 2>&1 &') %(namenode_ip,replication,blk_size)

print "<h1>20%</h1>"
if os.system(s) > 0:   ######test it for the errors
  sys.exit("<h1>exit here</h1>")

''' 
now we need to ssh and start the command and check for the exit code to confirm namenode setup			
'''

"setting up jobtracker"
jobtracker_ip = '127.0.0.1'
s = ('jobtracker.py %s %s %s > /dev/null 2>&1 &') % (namenode_ip,jobtracker_ip,scheduler)
if os.system(s) > 0:   ######test it for the errors
  sys.exit(1)

print "<h1>40%</h1>"
"setting up datanode"

a = ('datanode.py %s %s  > /dev/null 2>&1 &') %(namenode_ip,heartBeat)
  
tempFn = lambda x: os.system(x) 
thread.start_new_thread( tempFn, (a,) )
  
print "<h1>75%</h1>"
"setting up tasktracker"

a = ('tasktracker.py %s %s  > /dev/null 2>&1 &') %(namenode_ip,jobtracker_ip)
tempFn = lambda x: os.system(x) 
thread.start_new_thread( tempFn, (a,) )

  
print "<h1>100%</h1>"
print "Wait for few moments..."

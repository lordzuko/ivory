#!/usr/bin/python2

import os
import cgi
import cgitb
cgitb.enable()
print 'Content-type: text/html'
print '\n'

_file = open("data_conn.txt","r")
s=_file.readline();
_file.close();
 
print s+"<i class=\"icon-hdd\"></i>"

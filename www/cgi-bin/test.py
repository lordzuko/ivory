#!/usr/bin/python2

import cgi
import cgitb
cgitb.enable()

print 'Content-type: text/html'
print '\n'

form = cgi.FormContent()

name = form['namee']
email = form['email']
beer=[]
for i in range (len(name)):
  a = "beer"+str(i)
  beer.append(form[a])


for i in range(len(name)):
  print "<h1>"+name[i]+"</h1>"
  print "<h1>"+email[i]+"</h1>"
  for j in beer[i]:
  	print "<h1>"+j+"</h1>"

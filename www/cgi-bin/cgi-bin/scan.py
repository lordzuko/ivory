#!/usr/bin/python

import cgi
import cgitb
import os
import thread
import commands
cgitb.enable()

print "Content-type: text/html\n"

class g:
	def __init__(self):
		self.j=0
	def inc(self):
		self.j+=1

a=g()

data=cgi.FieldStorage()

ram=data['ram'].value
hd=data['hd'].value
cpu=data['cpu'].value
net=data['net'].value

#print ram
#print net

#-----------------------scan each ip------------------------------#
def scan(ip):
	check='''sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'''+ip
	check_status=os.system(check)
	if check_status==0:
		scanned={}
		scanned['ip']=ip
		print ip+'</br>'
	#a.inc()
		os.system('mkdir -p data/'+ip)
		ssh="sshpass -p 'redhat' ssh -o StrictHostKeyChecking=no root@"+ip
	#print ssh + '  mkdir temp'
		os.system(ssh + '  mkdir temp')
	#---------------HD----------------#
	
	#print ssh + '  parted -l /dev/sda > /root/temp/hd.txt'
		co='''sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'''+ip+''' "echo -e 'print\nq\n' | parted /dev/sda > /root/temp/hd.txt"'''
		os.system(co)
	###########SCP[/root/temp/hd.txt --> data/ip/]#################
		os.system("sshpass -p 'redhat' scp -o StrictHostKeyChecking=no root@"+ip+":/root/temp/hd.txt data/"+ip)
		dic={}
		with open('data/'+ip+'/hd.txt') as f:
			i=0
			for each in f:
				dic[i]=each
				i+=1
		mx_len=len(dic[5].split()[2])
		mx=int(float(dic[5].split()[2][0:mx_len-2]))
		mn_len=len(dic[i-3].split()[2])
		mn=int(float(dic[i-3].split()[2][0:mn_len-2]))
		rem=mx-mn
		scanned['hd']=rem

	#-------------------RAM----------------#
	
		os.system("sshpass -p 'redhat' ssh -o StrictHostKeyChecking=no root@"+ip+" 'free -m | grep Mem > /root/temp/ram.txt'")
	######SCP[/root/temp/ram.txt --> data/ip/]#############
		os.system("sshpass -p 'redhat' scp -o StrictHostKeyChecking=no root@"+ip+":/root/temp/ram.txt data/"+ip)
		with open('data/'+ip+'/ram.txt') as f:
			d=f.readline().split()[1]
		scanned['ram']=d

	#-------------------cpu-------------------#
	
		os.system("sshpass -p 'redhat' ssh -o StrictHostKeyChecking=no root@"+ip+" 'cat /proc/cpuinfo | grep processor | wc -l > /root/temp/cpu.txt'")
	######SCP[/root/temp/cpu.txt --> data/ip/]#############
		os.system("sshpass -p 'redhat' scp -o StrictHostKeyChecking=no root@"+ip+":/root/temp/cpu.txt data/"+ip)
		with open('data/'+ip+'/cpu.txt') as f:
			d=f.readline()[0:1]
		scanned['cpu']=d
		print str(scanned)+"</br>"
		flag=1
		if int(ram) > int(scanned['ram']):
			flag=0
		elif int(hd) > int(scanned['hd']):
			flag=0
			print str(scanned['ip'])+'_scan</br>'
		elif int(cpu) > int(scanned['cpu']):
			flag=0

		if flag==1:
			with open('elig.txt','a') as fl:
				fl.write(ip+'\n')
	a.inc()
#thread.start_new_thread(scan,('192.168.122.2',))
#scan('192.168.122.2')

#-------------------------network scan---------------------------#

def find_ip(network):
	os.system('sudo nmap -sP '+network+' | grep report > ip.txt')
	with open('ip.txt') as f:
		for each in f:
			length_list=len(each.split())
			if length_list==6:
				x=each.split()[5]
				y=len(x)-1
				ip=x[1:y]
				host=len(ip.split('.')[3])
			#print type(host)
				if host < 3:
					with open('ip_to_scan.txt','a') as ips:
						ips.write(ip+'\n')


find_ip(net)			#scan(ip)

with open('ip_to_scan.txt') as s:
	for each_ip in s:
		#print each_ip
		le=len(each_ip)
		thread.start_new_thread(scan,(each_ip[:le-1],))
				#print ip


it=int(commands.getoutput('cat ip_to_scan.txt | wc -l'))
while True:	
	if a.j<it:
		pass	
	else:	
		break
#------------------------------NODES--------------------------#
try:
	print "<pre> select namenode                    select datanode</br>"
	print "<form action='config.py' method='POST'>"
	with open('elig.txt') as hv:
		for each_ip in hv:
			lent=len(each_ip)
			print "<input name='nn' type='checkbox' value="+each_ip+" \>"+each_ip[:lent-1]+"                         <input name='dn' type='checkbox' value="+each_ip+" \>"+each_ip[:lent-1]+"</br>"

	print "<input type='submit' value='create' \></form></pre>"
except:
	print "no host"




#!/usr/bin/python

import cgi
import cgitb
import os
import thread
import commands
import crypt
cgitb.enable()

print "Content-type: text/html\n"

class g:
	def __init__(self):
		self.j=0
	def inc(self):
		self.j+=1

a=g()

data=cgi.FieldStorage()

nis=data['nis'].value
nfs=data['nfs'].value
#fil=data['up']
#nis='192.168.122.1'
#nfs='192.168.122.1'
print "nis: "+nis+'</br>'
print "nfs: "+nfs+'</br>'
#print fil

#file_quota='100'
#space_quota='10m'
ip_namenode=commands.getoutput('cat namenodes.txt')
os.system("echo -e 'domain hadoop server "+nis+"' | cat >> nis/yp.conf")
#os.system("sudo echo 'NISDOMAIN=hadoop' | cat >> /etc/sysconfig/network")
#os.system("sudo sed -i 's/\/misc/\/home/g' nis/auto.master")
os.system("echo -e '*	"+nfs+":/user/&' | cat >> nis/auto.misc")
os.system("sudo echo -e 'PATH=/usr/java/jdk1.7.0_51/bin:$PATH  export PATH'| cat >> hadoop/.bashrc")
os.system("sudo sed -i '/<configuration>/a <property><name>fs.default.name</name><value>hdfs://"+ip_namenode+":9001</value></property>' hadoop/core-site.xml")

os.system('sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+ip_namenode+' "hadoop fs -mkdir /user"')

#####---------------------------NIS------------------------------######

with open('users.txt') as u:
	for each in u:
		user_name=str(each.split(':')[0])
		password=str(each.split(':')[1])
		file_quota=str(each.split(':')[2])
		space_quota=str(each.split(':')[3])
		print "</br>"+user_name+":"+password+":"+file_quota+":"+space_quota+"</br>"
		x=os.system("sshpass -p 'redhat' ssh -o StrictHostKeyChecking=no root@"+nis+" 'useradd "+user_name+"'")
		print x
		cmd_pas='''sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'''+nis+''' "echo  -e '''+password+'''| passwd '''+user_name+''' --stdin" &> /dev/null'''
		#print cmd_pas		
		os.system(cmd_pas)
		#print str(x)+"</br>"
		os.system('sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+nfs+' "mkdir -p /user/'+user_name+'; cp -rf /etc/skel/. /user/'+user_name+'"')
		os.system('sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+nfs+' "mkdir -p /user/'+user_name+'; cp -rf /etc/skel/. /user/'+user_name+'"')
		os.system('sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+ip_namenode+' "hadoop fs -mkdir /user/'+user_name+'; hadoop fs -chown  '+user_name+':'+user_name+' /user/'+user_name+'; hadoop fs -chmod 770 /user/'+user_name+'"')
		os.system('sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+ip_namenode+' "hadoop dfsadmin -setQuota '+file_quota+' /user/'+user_name+'"')
		os.system('sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+ip_namenode+' "hadoop dfsadmin -setSpaceQuota '+space_quota[:3]+' /user/'+user_name+'"')
		#print 'sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+ip_namenode+' "hadoop dfsadmin -setSpaceQuota '+space_quota+' /user/'+user_name+'"</br>'
		#print str(x)+"......."
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~sed on /etc/shadow~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
os.system('sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+nis+' "yum install ypserv --quiet -y" &> /dev/null')

os.system('sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+nis+' "ypdomainname hadoop"')

os.system('sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+nis+' "service ypserv stop;service ypserv start" &> /dev/null')

os.system('sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+nis+' "make -C /var/yp" &> /dev/null')

####--------------------------NFS-----------------------------##########

os.system('sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+nfs+' "yum install nfs-utils --quiet -y" &> /dev/null')


exp='''sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'''+nfs+''' "echo '/user   *(rw,sync)' | cat >> /etc/exports"'''

os.system(exp)

os.system('sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+nfs+' "service nfs restart"')

######--------------------------client---------------------------#######
def install(ip):
	os.system("sshpass -p 'redhat' ssh -o StrictHostKeyChecking=no root@"+ip+" 'setenforce 0;iptables -F'")
	a.inc()
	os.system('sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+ip+' "yum install ypbind --quiet -y" &> /dev/null')

def client_conf(ip):
	#------------------------------------/etc/sysconfig/network-------------------------------------#
	cmd_net='''sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'''+ip+''' "sed -i '/HOSTNAME/a NISDOMAIN=hadoop' /etc/sysconfig/network"'''
	os.system(cmd_net)
	#---------------------------------------/etc/yp.conf--------------------------------------------#
	cmd_yp='''sudo sshpass -p "redhat" scp -o StrictHostKeyChecking=no nis/yp.conf '''+ip+''':/etc/'''
	os.system(cmd_yp)	
	#--------------------------------------/etc/nsswitch.conf---------------------------------------#
	cmd_yp='''sudo sshpass -p "redhat" scp -o StrictHostKeyChecking=no nis/nsswitch.conf '''+ip+''':/etc/'''
	os.system(cmd_yp)

	#------------------------------------/etc/pam.d/system-auth-------------------------------------#
	cmd_pam='''sudo sshpass -p "redhat" scp -o StrictHostKeyChecking=no nis/system-auth '''+ip+''':/etc/pam.d/'''
	os.system(cmd_pam)
	#---------------------------------- /etc/pam.d/system-auth-ac-----------------------------------#
	cmd_pam_ac='''sudo sshpass -p "redhat" scp -o StrictHostKeyChecking=no nis/system-auth-ac '''+ip+''':/etc/pam.d/'''
	os.system(cmd_pam_ac)
	os.system('sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+ip+' "service ypbind stop;service ypbind start" &> /dev/null')
	#a.inc()
	####----------------------------autofs------------------------------########

	os.system('sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+ip+' "yum install autofs --quiet -y" &> /dev/null')
	
	misc='''sudo sshpass -p "redhat" scp -o StrictHostKeyChecking=no nis/auto.misc '''+ip+''':/etc'''
	os.system(misc)

	master='''sudo sshpass -p "redhat" scp -o StrictHostKeyChecking=no nis/auto.master '''+ip+''':/etc'''
	os.system(master)

	os.system('sshpass -p "redhat" ssh -o StrictHostKeyChecking=no root@'+ip+' "service autofs stop; service autofs start" &> /dev/null')
	a.inc()
	###-------------------------------hadoop-----------------------------#########
	"""os.system("sshpass -p 'redhat' ssh -o StrictHostKeyChecking=no root@"+ip+" 'yum install jdk --quiet -y hadoop --quiet -y' &> /dev/null")
	os.system("sudo sshpass -p 'redhat' scp -o StrictHostKeyChecking=no hadoop/core-site.xml "+ip+":/etc/hadoop/")"""
	

with open('ip_to_scan.txt') as f:
	for each in f:
		le=len(each)
		client_ip=each[:le-1]
		thread.start_new_thread(install,(client_ip,))		
		thread.start_new_thread(client_conf,(client_ip,))


it=int(commands.getoutput('cat ip_to_scan.txt | wc -l'))
while True:	
	if a.j<2*it:
		pass	
	else:	
		os.system('rm -rf nis;cp -rf nis_backup nis')
		os.system('rm -rf hadoop;cp -rf backup hadoop')
		break

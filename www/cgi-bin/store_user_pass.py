import sys
import hashlib
import getpass
import os
def main(argv):

	if len(argv) != 2:
		sys.exit('Usage: store_user_pass.py <file_name or username> <password>')

	print '\nUser & Password Storage Program v.01\n'
'''	
	if raw_input('The file ' + sys.argv[1] + ' will be erased or overwrite if exsting.\nDo you wish to continue (Y/n): ') not in ('Y','y') :
		sys.exit('\nChanges were not recorded\n')
'''
	#user_name = raw_input('Please Enter a User Name: ')
        if os.system("test -f"+argv[0]) == 0:
                return 1
	password = hashlib.sha224(getpass.getpass(argv[1]).hexdigest()
	

	try:
		file_conn = open(sys.argv[1],'w')
		file_conn.write(user_name + '\n')
		file_conn.write(password + '\n')
		file_conn.close()
	except:
		sys.exit('There was a problem writing to the file!')

	print '\nPassword safely stored in ' + sys.argv[0] + '\n'		
			
if __name__ == "__main__":
	main(sys.argv[1:])

import os
import paramiko
import time
import lxml.etree as ET

#Function to upload and execute the client script by SSH
def upload_script(ip,port, user, passwd,OS):
	try:

 	 	ssh = paramiko.SSHClient() 
	 	ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
	 	ssh.connect(ip,port, username=user, password= passwd)#SSH connection
 		sftp = ssh.open_sftp()
                if OS == "Windows":#If the host is Windows, the script is going to upload Windows Client
 			sftp.put('Windows_client.py', "Windows_client.py")# This line put the client on the root of the server sftp, in order to work it must be %temp% .I installed freessh on Windows
 			stdin, stdout, stderr = ssh.exec_command( r"python C:\Users\Administrator\AppData\Local\Temp\2\Windows_client.py") #execute the script in this folder
                        print "Script executed successfully on " +ip                         
		else:
                         os.system("scp Linux_client.py "+user+"@"+ip+":/")#Use module OS to uploaad the script in Linux
       			 stdin, stdout, stderr = ssh.exec_command( r"python /Linux_client.py") #Please guarantee the privilege on the client to copy and execute the script
                        
                sftp.close()
 		ssh.close()

	except paramiko.AuthenticationException:
 		print "Authentication failed when connecting to " + ip
          
 		sys.exit(1)
	except:
  		print "Something is wrong, please check it on  " + ip
          
  		time.sleep(2)

#This function parse the file config.xml using XPATH to extract all the data to upload the script in the IPs.
def get_xml_data():
        tree = ET.parse("config.xml")
        root = tree.getroot()
        path="/data/client/@ip"   #Extract all the IPs
        results= root.xpath(path)
        length = len (results)

        users =[None]*length       #Initialize the lists to save all the data of the config.xml
        passwords=[None]*length
        ports=[None]*length
        OSs=[None]*length
        for i in range(0, length):
            path="/data//client[@ip='"+results[i]+"']/username/text()" #XPath to parse USERNAME
            username=root.xpath(path)
            users[i]=username
            path="/data//client[@ip='"+results[i]+"']/password/text()" #XPath to parse PASSWORD
            password=root.xpath(path)
            passwords[i]=password
            path="/data//client[@ip='"+results[i]+"']/port/text()"  #XPath to parse PORT
            port=root.xpath(path)
            ports[i]=port
            path="/data//client[@ip='"+results[i]+"']/OS/text()"  #XPath to parse OS
            OS=root.xpath(path)
            OSs[i]=OS
        return results,ports,users,passwords,OSs



results = get_xml_data() # Parse all the data in config.xml
num_items= len(results[0])


#loop to coonect to all the clients in config.xml
for i in range (0, num_items):
     ip= results[0][i]

     port=str(results[1][i])
     port=port.strip('[]')      #Strip characters such as [] " '
     port=port.replace("'", "")
     port=int(port)

     user=str(results[2][i])
     user=user.strip('[]')
     user=user.replace('"', "")   #Strip characters such as [] " '
     user=user.replace("'", "")

     passwd=str(results[3][i])
     passwd=passwd.strip('[]')
     passwd=passwd.replace('"', "")    #Strip characters such as [] " '
     passwd=passwd.replace("'", "")

     OS=str(results[4][i])
     OS=OS.strip('[]')
     OS=OS.replace('"', "")  #Strip characters such as [] " '
     OS=OS.replace("'", "")

     print "Uploading the script..."
     upload_script(ip,port, user, passwd,OS) # Function toupload the script





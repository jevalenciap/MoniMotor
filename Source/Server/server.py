import socket
import sys
import time
from thread import *
from CypherClass import AESCipher
import lxml.etree as ET
import yagmail
import MySQLdb

# function to get the CPU alert value in the config.xml file using XPATH
def alert_value_cpu(ip):
	tree = ET.parse("config.xml")
  	root = tree.getroot()
        path="/data//client[@ip='"+ip+"']/alert[@type='cpu']/@limit"
        o= root.xpath(path)
        return o[0]

# function to get the Memory alert value in the config.xml file using XPATH
def alert_value_ram(ip):
        tree = ET.parse("config.xml")
        root = tree.getroot()
        path="/data//client[@ip='"+ip+"']/alert[@type='memory']/@limit"
        o= root.xpath(path)
        return o[0]

#function to write the client recieved data on a file named logs
def write_log_file(ip, av):
        file = open( "logs", "a")
        file.write( ip + " ")
        file.write( av +'\n')
        
#funtion to get the email in config.xml using XPATH
def get_mail(ip):
        tree = ET.parse("config.xml")
        root = tree.getroot()
        path="/data//client[@ip='"+ip+"']/mail/text()"
        mail=(root.xpath(path))
        mail=mail[0]
        mail=mail.replace('"', "")
        return mail

#function to send RAM email alert using yagmail module
def send_mail_ram(mail, value):
        yag = yagmail.SMTP('crossworktester', 'croosswork23')#Gmail account(user,pass) created for this project
        contents = ['Please review the RAM, the RAM  precent is: '+value]
        yag.send(mail, 'Alarm RAM', contents)

#function to send CPU email alert using yagmail module
def send_mail_cpu(mail, value):
        yag = yagmail.SMTP('crossworktester', 'croosswork23')
        contents = ['Please review the CPU, the CPU precent is: '+value]
        yag.send(mail, 'Alarm CPU', contents)



 
HOST = '172.31.55.49'   # Change!!!!- Server IP listening 
PORT = 6666 # Change!!! - Server Port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#Function for handling connections. This will be used to create threads
def clientthread(conn):

     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        print "Data encrypted received"
        print  data + "\n"
        
        #using class to decrypt the message
        Re= AESCipher("llave") # "llave" is the key to decrypt the message, it must be the same in the server and client
        av= Re.decrypt(data) 
        print "Data decrypted:"
        print av  + "\n"
       
        ip=str(addr[0]) # Get the Client IP
        write_log_file(ip, av) #Writing the data in log file 
        
  
        list =av.split(" ") #Saving the Client data in a list. 
        memory= list[0]  #Get memory value      
        cpu=list[1] #Get CPU value
        
                         
        ram_alarm= alert_value_ram(ip) #Get the RAM value alert in config.xml
        cpu_alarm= alert_value_cpu(ip) #Get the CPU value alert in config.xml
        
        #Compare the values
        if memory > ram_alarm :
         	   mail=get_mail(ip)
		   send_mail_ram(mail, memory) # send the email if is higher
                   print "RAM Email sent- Usage: " + memory + "\n"

        if cpu > cpu_alarm :
                   mail=get_mail(ip)
                   send_mail_cpu(mail, cpu)# send the email if is higher
                   print "CPU Email sent- Usage: " + cpu + "\n"

        reply= "OK" # SEND REPLY TO THE CLIENT
    
        conn.send(reply)


        #Please modify this values to connect to the database !!!
        #Connect to the database
        conn = MySQLdb.connect(host= "localhost",
                           user="root", 
                           passwd="76gb2j2*.YT", 
                           db="crosswork")
        x = conn.cursor()
         
        try:
            #Insert the values in the table named Logs      
         	x.execute('''INSERT into Logs (IP, CPU, RAM, OS,Total_SecurityEvents,EventCategory,TimeLastEvent, SourceName,EVENTID,EVENTYPE  ) values (%s, %s,%s, %s, %s, %s, %s, %s,%s, %s)''', (ip, cpu, memory, list[2],list[3],list[4],(list[5]+" "+list[6]),list[7],list[8],list[9]))
                print "OK...Data saved in the Database"

                conn.commit()
        except:
   		conn.rollback()

           	conn.close()
 


     
       
        if not data: 
            break
     
#        conn.sendall(reply)
     
    #came out of loop
    conn.close()
 
 
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    
 
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()


import psutil,datetime
import platform
import win32evtlog
import socket
import sys
import time
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


#I use this class to cipher the communication using AES
class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)) # The ciphertext is encoding -base64

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s): # Pad definition
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


#function to get the uptime
def uptime():
    p = psutil.Process()
    p.create_time()
    UPTIME=datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S")
    return UPTIME


#The CPU,RAM and uptime statistics are based on psutil module.
CPU=psutil.cpu_percent()  #get CPU percent
VMEM=psutil.virtual_memory()
RAM= VMEM.percent #get RAM percent
OS=platform.system() # get OS (Windows-Linux)

#print on the screen the values
print "Memory:", RAM
print "CPU:", CPU
print "OS: ", OS
print "Uptime since:", uptime()


#Get the last event security log using win32 and print on the screen
server = 'localhost'  # name of the target computer to get event logs
logtype = 'Security'
hand = win32evtlog.OpenEventLog(server, logtype)
flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
total = win32evtlog.GetNumberOfEventLogRecords(hand)
events = win32evtlog.ReadEventLog(hand, flags, 0)
if events:
    for event in events:

        print 'Total Security Events:', total
        print "The last event security log:"
        print 'Event Category:', event.EventCategory
        print 'Time Generated:', event.TimeGenerated
        print 'Source Name:', event.SourceName
        print 'Event ID:', event.EventID
        print 'Event Type:', event.EventType
        print  ""
        data = event.StringInserts

#save the data in a list
Data=[None] * 9
Data[0]= RAM
Data[1]=CPU
Data[2]=OS
Data[3]=total
Data[4]=event.EventCategory
Data[5]=event.TimeGenerated
Data[6]=event.SourceName
Data[7]=event.EventID
Data[8]=event.EventType

#Join/serialized all the values of the list in order to send the server
Serial_Data=''
for x in range(0,9):
    Serial_Data=Serial_Data+str(Data[x])+" "
print "Data before to encrypt:"
print Serial_Data +"\n"

#Connecet to the server creating a socket
HOST = '172.31.55.49'   # CHANGE - IP ADDRESS OF THE SERVER
PORT = 6666   # CHANGE - PORT OF THE SERVER
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#using the Class to cypher the serialized data
crom=AESCipher("llave")#"llave" is the key used to cypher the data, it must be the same in the client and server
cipher_message=crom.encrypt(Serial_Data)
s.send(cipher_message)#send data cypher
print "Data encrypted"
print cipher_message +"\n"

reply = s.recv(1024)#Waiting the ACK of the serever
if reply=='OK':
        print reply + "...Data recieved for the server"
        s.close()
        sys.exit()


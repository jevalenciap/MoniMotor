Readme.txt

1)Instructions to install and configure prerequisites or dependencies:

-Use pip to install the next dependencies in Python:

example (Linux): pip install yagmail
example Windows: python -m pip install yagmail 

*Server Python dependencies:
import socket
import sys
import time
from thread import *
import lxml.etree as ET
import yagmail
import MySQLdb
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


*Linux Client Python dependencies:
import psutil,datetime
import platform
import socket
import sys
import time
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

*Windows Client Python dependencies:
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


*script_upload_clients.py Python dependencies
import os
import paramiko
import time
import lxml.etree as ET


-Install freesshd on Windows clients 

Download link:
http://www.freesshd.com/?ctt=download

Configuration freessh:
http://www.techmalaya.com/2009/08/05/setup-ssh-server-for-windows-freesshd/

Please configure the SFTP Home Path: %temp%   (Very Important, because in this path the client is uploaded)

Test Connecting from another host by SSH.


2)Instructions to create and initialize the database:

Please follow the instructions in:
/source/server/Database
 

3)Please modify the config.xml according your hosts

4)I used yagmail module to send the alert emails, you can use the test account, that I have created.

5)Please give the permission on folder (/) in Linux hosts to upload and execute the script.   

6)Modify the server IP and port in the next scripts server.py (line 59,60), Windows_client.py(line 101,102), Linux_client.py(line 71,72)

7)You can modify the key(default value is "llave") to encrypt and decrypt the data in server.py (line 91), Windows_client.py(line 107), Linux_client.py(line 77). It must be the same in all the files.

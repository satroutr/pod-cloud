#!/usr/bin/python
import paramiko
import string
import webbrowser
import os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.64.72.65', username='cisco', password='cisco123') 
    
print "1: get file \n2: print contents of file"
c=2

if c==1:
    ftp = ssh.open_sftp()
    ftp.get('deplo.txt', 'deplo.txt')
    ftp.close()
    webbrowser.open_new(os.getcwd()+"/deplo.txt")
    print "FILE GOT!"
elif c==2:
    ftp = ssh.open_sftp()
    file=ftp.file('deploy.cfg', "r", -1)
    data=file.read()
    string = string.split(data)
    print string
#     if 'ipaddress' in string:
#         print string
#     L = string.split(data)
#     print L
#     for i in L:
#         if string.find(i, '%')>-1:
#             print i
#     print ftp.stat("deplo.txt")        
    ftp.close()
    print "DONE!"   
else: 
    print "EXIT!"
ssh.close()
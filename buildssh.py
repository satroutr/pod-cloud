#!/usr/bin/env python
import sys
import socket
from ssh import SSHClient
import ssh
import ConfigParser
from time import sleep

class MySSH:
    
    def __init__ (self):
        self.ssh = None
        self.transport = None 
    def connect(self):
        config = ConfigParser.ConfigParser()
        config.read("config.ini")
        client = SSHClient()
        client.set_missing_host_key_policy(ssh.AutoAddPolicy())
        hostname = config.get("host", "hostip")
        print "sshing to %s:", hostname
        username = config.get("host", "username")
        password = config.get("host", "password")
    def runcommands(connect):
        client.connect(hostname, username=username, password=password)
        stdin, stdout, stderr = client.exec_command('sudo apt-get update')
        print "stderr: ", stderr.readlines()
        print stdout.readlines()
        stdin, stdout, stderr = client.exec_command('brctl show')
        print "stderr: ", stderr.readlines()
        out = stdout.readlines()
        print out
c = MySSH()
c.runcommands()
# stdin, stdout, stderr = client.exec_command('sudo ifconfig br0 down')
# print "stderr: ", stderr.readlines()
# out = stdout.readlines()
# print out
# stdin, stdout, stderr = client.exec_command('sudo brctl delbr br0')
# print "stderr: ", stderr.readlines()
# out = stdout.readlines()
# print out
# stdin, stdout, stderr = client.exec_command('sudo apt-get autoremove -y pod-cloud-installer')
# print "stderr: ", stderr.readlines()
# print stdout.readlines()
# stdin, stdout, stderr = client.exec_command('sudo apt-get update')
# print "stderr: ", stderr.readlines()
# print stdout.readlines()
# stdin, stdout, stderr = client.exec_command('sudo apt-get install -y pod-cloud-installer')
# print "stderr: ", stderr.readlines()
# print stdout.readlines()
# stdin, stdout, stderr = client.exec_command('pod-cloud-installer -c ~/deploy.cfg --all')
# print "stderr: ", stderr.readlines()
# print stdout.readlines()
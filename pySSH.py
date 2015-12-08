#!/usr/bin/env python
import sys
import socket
import paramiko
import ConfigParser
from time import sleep
#=================================
# Class: PySSH
#=================================
class pySSH(object):
   
   
    def __init__ (self):
        self.ssh = None
        self.transport = None
        self.ftp = None 
 
    def disconnect (self):
        if self.transport is not None:
           self.transport.close()
        if self.ssh is not None:
           self.ssh.close()
 
    def connect(self,hostname,username,password,port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
 
        self.ssh = paramiko.SSHClient()
        #Don't use host key auto add policy for production servers
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.load_system_host_keys()
        try:
            self.ssh.connect(hostname,port,username,password)
            self.transport=self.ssh.get_transport()
        except (socket.error,paramiko.AuthenticationException) as message:
            print "ERROR: SSH connection to "+self.hostname+" failed: " +str(message)
            sys.exit(1)
        return  self.transport is not None
 
    def execute(self,cmd,sudoenabled=False):
        if sudoenabled:
            fullcmd="echo " + self.password + " |   sudo -S -p '' " + cmd
        else:
            fullcmd=cmd
        if self.transport is None:
            return "ERROR: connection was not established"
        session=self.transport.open_session()
        session.set_combine_stderr(True)
        #print "running command: "+fullcmd
        if sudoenabled:
            session.get_pty()
        session.exec_command(fullcmd)
        stdout = session.makefile('rb', -1)
        #print stdout.readlines()
        #print stdout.read()
        output=stdout.read()
        #print output+ "Here"*10
        session.close()
        return output
    def _open(self):
        """open a scp channel"""
        if self.channel is None:
            self.channel = self.transport.open_session()
    def scp_put_file(self, local_file, remote_file):
        """
        Copies a file from local to remote using FTP
        :param remote_file: Path to remote file
        :param local_file: Path to local file
        :return: Returns boolean to show whether transfer succeeded
        """
        if self.ftp is None:
            self.ftp = self.ssh.open_sftp()
        self.ftp.put(local_file, remote_file)
        return True
if __name__ == '__main__':
    pass
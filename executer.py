#!/usr/bin/python
import sys
import socket
from pySSH import pySSH
import ConfigParser
from time import sleep
import subprocess
import os
import paramiko
from IPMItool import IPMItool
config = ConfigParser.ConfigParser()
config.read("config.ini")

'''Getting the details from config file'''

hostname = config.get("buildnode", "hostip")
username = config.get("buildnode", "username")
password = config.get("buildnode", "password")
cimcip = config.get("ipmi", "cimcaddress")
cimcuser = config.get("ipmi", "cimcusername")
cimcpassword = config.get("ipmi", "cimcpassword")

'''powering down the nodes'''
ipmi = IPMItool()
#print cimcip
cimcaddresses = cimcip.split(",")
 
for cimcaddress in cimcaddresses:
    print cimcaddress
    ipmi.connect(cimcaddress,cimcuser,cimcpassword)
    systemstatus = ipmi.execute("chassis power off")
    print ipmi.output
ssh = pySSH()

'''ssh to the build node'''

ssh.connect(hostname,username,password)
print "SSHing to Host: " + hostname + " with username: " + username + " and password: " + password
systemtime = ssh.execute('date')
print systemtime

'''installing ipmi tool on build node'''

installipmi = ssh.execute('apt-get install -y ipmitool',True )

''' Adding the repos to pull pod-cloud-installer'''

addcommonpackage = ssh.execute('apt-get install -y software-properties-common',True)
addrepo = ssh.execute('add-apt-repository "deb https://landscape-cisco:p0NSJJ3gNSV8FLRJXrlC@private-ppa.launchpad.net/landscape/lds-cisco-odl-release/ubuntu trusty main"', True)
addkey = ssh.execute('sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key 6E85A86E4652B4E6',True)
update=ssh.execute('apt-get update',True)
'''Installing openstack clients to bootstrap'''

addnovaclient = ssh.execute('apt-get install -y python-novaclient',True)
addglanceclient = ssh.execute('apt-get install -y python-glanceclient',True)
addneutronclient = ssh.execute('apt-get install -y python-neutronclient',True)
addcinderclient = ssh.execute('apt-get install -y python-cinderclient',True)
addkeystoneclient = ssh.execute('apt-get install -y python-keystoneclient',True)

'''Adding nopassword to sudoers'''



'''deleting the bridge if present then recreating the bridge'''

bridgelist = ssh.execute('brctl show',True)
 #print bridgelist
getbridge = ssh.execute('ifconfig | grep br0',True)
if getbridge == "":
    print "br0 is not present"
else:
    print "br0 is present, details are %s, deleting the bridge" % getbridge
    downbridge = ssh.execute('ifconfig br0 down',True)
    delbridge = ssh.execute('brctl delbr br0',True)
update=ssh.execute('apt-get update',True)

'''installing the latest pod cloud installer '''

ifinstalled = ssh.execute('pod-cloud-installer --version')
print ifinstalled
if "command not found" in ifinstalled:
    print "pod-cloud-installer is not installed. Installing pod-cloud-installer"
else:
    print "pod-cloud-installer version %s is installed. removing the pod-cloud-installer" % ifinstalled
    removing = ssh.execute('apt-get autoremove -y pod-cloud-installer', True)
 #print "printing output of purge"
install = ssh.execute('apt-get install -y pod-cloud-installer', True)
ifinstalled = ssh.execute('pod-cloud-installer --version')
if ifinstalled == "pod-cloud-installer: command not found":
    print "Fail:pod-cloud-installer is not installed"
    raise Exception("Fail: pod-cloud-installer failed to install")
else:
    print "pod-cloud-installer version %s is installed." % ifinstalled
  
 #print "installing pod-cloud-installer"
ssh.disconnect()

'''running the deploy config to install openstack on nodes'''

ssh.connect(hostname,username,password)
print "SSHing to Host: " + hostname + " with username: " + username + " and password: " + password
ssh.scp_put_file('deployconfig', 'deploy.cfg')
print "Starting installation of Openstack wait for 4 hours"
installingopenstack = ssh.execute('pod-cloud-installer -c deploy.cfg --all', False)
sleep(30)
installingopenstack = ssh.execute('pod-cloud-installer -c deploy.cfg --all', False)
print installingopenstack

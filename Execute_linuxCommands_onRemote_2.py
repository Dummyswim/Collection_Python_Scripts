#!/usr/bin/python
import fileinput
import sys
import paramiko as pm
import os

sys.stderr = open('/dev/null')       # Silence silly warnings from paramiko
sys.stderr = sys.__stderr__


class AllowAllKeys(pm.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return

with open('host.txt', 'r') as f:
    for host in f:
        HOSTN = host.rstrip()
        USER = 'myuser'
        PASSWORD = 'mypass'

        client = pm.SSHClient()
        client.load_system_host_keys()
        client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        client.set_missing_host_key_policy(AllowAllKeys())
        client.connect( HOSTN, username=USER, password=PASSWORD )

        channel = client.invoke_shell()
        stdin = channel.makefile('wb')
        stdout = channel.makefile('rb')

        stdin.write('''
        hostname
        lsb_release -a
        exit
        ''')
        print stdout.read()

        stdout.close()
        stdin.close()
        client.close()
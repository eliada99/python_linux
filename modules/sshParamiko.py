#!/usr/bin/python

import paramiko


def ssh_command(ip, command):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try :
        client.connect(str(ip), port=22, username="root", password="3tango")
    except :
        ip, "error : ssh connection failed"
        return ip, "error : ssh connection failed"
    stdin, stdout, stderr = client.exec_command(str(command))
    stdout = stdout.read()
    stderr = stderr.read()
    client.close()
    if stderr: return ip,"error : %s" % stderr
    else: return ip, stdout

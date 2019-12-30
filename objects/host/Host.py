#!/usr/bin/python
"""
@ By Eliad Avraham - eliada@mellanox.com / eliadush9@gmail.com / +972-5136306
"""
import re
import subprocess

from modules import utilities
from objects.RemoteConnection import RemoteConnection


class Host(object):
    def __init__(self, ip):
        self.ip = ip
        self.last_output = None
        remote = RemoteConnection()
        conn = remote.connect(ip)
        # conn = remote.connect_to_arm(ip) # see limitation in ReadMe.txt file
        self.conn = None if conn is None else conn
        self.machine_type = conn.modules.platform.system()  # Returns the system/OS name, e.g. 'Linux', 'Windows'
        self.processor_name = conn.modules.platform.processor()  # Returns the processor name, e.g. 'amdk6' / 'x86_64'
        self.hostname = conn.modules.platform.node()  # returns the host name, e. g 'bfhp12'
        self.os_details = conn.modules.platform.platform(aliased=0, terse=0)  # 'Linux-3.10.0-693.el7.x86_64-x86_64-with-redhat-7.4-Maipo'
        self.linux_distribution = conn.modules.platform.linux_distribution()[0]  # 'Red Hat Enterprise Linux Server'

    # Getters methods
    def get_conn(self):
        return self.conn

    def get_ip(self):
        return self.ip

    def get_machine_type(self):
        return self.machine_type

    def get_processor_name(self):
        return self.processor_name

    def get_os_details(self):
        return self.os_details

    def get_linux_distribution(self):
        return self.linux_distribution

    def get_hostname(self):
        return self.hostname

    def get_last_output(self):
        return self.last_output

    # run command function
    # self = remoteConnection object
    # cmd = your command
    # reg = with/without regex to pull only the needed output
    # return_value = with/without return value
    def run_cmd(self, cmd, reg, return_value=0):
        if hasattr(self, 'hostname'):
            host = self.get_hostname()
        else:
            host = "No Name Yet"
        utilities.reporter("Function: HostLinux.run_cmd, Object: HostLinux: " + host + "\nCommand: " + cmd + "\n",
                           'green')
        proc = self.conn.modules.subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                  universal_newlines=True)
        stdout, stderr = proc.communicate()

        if stderr:
            utilities.reporter("Something went wrong: " + stderr, 'red')
            self.last_output = stderr  # need to verify it
            raise Exception("failed in command: " + cmd)
            return None
        utilities.reporter("Output of command is: " + stdout, 'blue')
        self.set_last_output(stdout)
        if reg:
            try:
                stdout = re.findall(reg, stdout)[0]
            except:
                utilities.reporter("Host: " + self.get_hostname() + "Command Fail: " + cmd + "\n" + stdout, 'red')
                return None
        # if cmdStatus: return None
        if return_value:
            return stdout

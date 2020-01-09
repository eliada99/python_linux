#!/usr/bin/python

import utilities

INSTALLATION_LOG = "/tmp/installation_log.txt"


def driver_action(host_obj, action):
    cmd = "etc/init.d/openibd " + action
    try: return host_obj.run_cmd(cmd, 0, 1, 1)
    except:
        utilities.reporter("Driver action failed: " + cmd + "\n", 'red')
        return None


def install_driver(host_obj, action):
    try:
        host_obj.run_cmd(action, 0, 1, 1, INSTALLATION_LOG)
        action = 'cat ' + INSTALLATION_LOG + " | grep -i '/etc/init.d/openibd restart'"
        res = host_obj.run_cmd(action, 0, 1, 1)
        if res: return True
        else: return False
    except:
        utilities.reporter("install failed: " + action + "\n", 'red')
        return False

#!/usr/bin/python

import utilities


def driver_action(host_obj, action):
    cmd = "etc/init.d/openibd " + action
    try:
        return host_obj.run_cmd(cmd, 0, 1, 1)
    except:
        utilities.reporter("Driver action failed: " + cmd + "\n", 'red')
        return None

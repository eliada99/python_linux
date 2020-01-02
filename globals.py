#!/usr/bin/python
"""
@ By Eliad Avraham - eliada@mellanox.com / eliadush9@gmail.com / +972-5136306
This file is saving the mainly globals parameters in my project
"""
import threading
import json

from objects.host.HostLinux import HostLinux
from objects.HostInterfaceEth import HostInterfaceEth
from objects.HostHca import HostHca
from tests.Runner import Runner
from modules import RunInParallel

JSON_FILE = "json_file.json"

global hostLinuxServer, hostLinuxClient, serverInterfaceEth1, serverInterfaceEth2
global clientInterfaceEth1, clientInterfaceEth2, serverHca, clientHca, setupObjTuple
global runner

def init():
    # save objects as globals for all project
    global hostLinuxServer, hostLinuxClient, serverInterfaceEth1, serverInterfaceEth2
    global clientInterfaceEth1, clientInterfaceEth2, serverHca, clientHca, setupObjTuple
    global runner

    objects_list = []

    with open(JSON_FILE) as f:
        json_file = json.load(f)
        f.close()

    if json_file["GUI"]["gui"]["value"]:
        runner = Runner()

    setup = create_objects_in_parallel(json_file["setup"]["server"]["value"], json_file["setup"]["client"]["value"])
    for i in setup:
        objects_list.append(i.instance)

    hostLinuxServer = objects_list[0]
    hostLinuxClient = objects_list[1]

    interfaces = json_file["setup"]["server_interfaces"]["value"].split(',')
    serverInterfaceEth1 = HostInterfaceEth(hostLinuxServer, interfaces[0])
    serverInterfaceEth2 = HostInterfaceEth(hostLinuxServer, interfaces[1])

    interfaces = json_file["setup"]["client_interfaces"]["value"].split(',')
    clientInterfaceEth1 = HostInterfaceEth(hostLinuxClient, interfaces[0])
    clientInterfaceEth2 = HostInterfaceEth(hostLinuxClient, interfaces[1])

    serverHca = HostHca(hostLinuxServer, serverInterfaceEth1, serverInterfaceEth2)
    clientHca = HostHca(hostLinuxClient, clientInterfaceEth1, clientInterfaceEth2)
    setupObjTuple = (hostLinuxServer, hostLinuxClient, serverHca, clientHca)


# ---------- Start of SomeThread class ------
class SomeThread(threading.Thread):
    def __init__(self, ip):
        try:
            threading.Thread.__init__(self)  # create Thread object
            self.ip = ip
        except Exception as err:
            raise Exception("Thread fail:" + ip + " " + err)

    def run(self):
        self.instance = HostLinux(self.ip)
        if self.instance is None:
            self.instance = None


# create HostLinux objects according the inputs, in parallel, and return the list objects to main
def create_objects_in_parallel(server, client):
    setup = []
    for host in server, client:  # start from the second cell - first cell contain the script name
        t = SomeThread(host)
        t.start()  # execute the run() def
        setup.append(t)
    for t in setup:
        t.join()  # timeout - Wait until the thread terminates
    print("-----------------------------------------")
    print('-------- All Threads are done! ----------')
    print("-----------------------------------------\n\n")
    return setup

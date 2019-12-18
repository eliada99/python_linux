#!/usr/bin/python
import sys
import threading  # https://docs.python.org/2/library/threading.html

from objects.HostLinux import HostLinux
from objects.HostInterfaceEth import HostInterfaceEth
from objects.HostHca import HostHca


'''this file is saving the main globals parameters in my project'''


def init():
    # save objects - should be in globals
    global hostLinuxServer, hostLinuxClient, serverInterfaceEth1, serverInterfaceEth2
    global clientInterfaceEth1, clientInterfaceEth2, serverHca, clientHca, setupObjTuple

    objects_list = []
    setup = create_objects_in_parallel()
    for i in setup:
        objects_list.append(i.instance)

    hostLinuxServer = objects_list[0]
    hostLinuxClient = objects_list[1]
    serverInterfaceEth1 = HostInterfaceEth(hostLinuxServer, "eth2")
    serverInterfaceEth2 = HostInterfaceEth(hostLinuxServer, "eth3")
    clientInterfaceEth1 = HostInterfaceEth(hostLinuxClient, "eth4")
    clientInterfaceEth2 = HostInterfaceEth(hostLinuxClient, "eth5")
    serverHca = HostHca(hostLinuxServer, serverInterfaceEth1, serverInterfaceEth2)
    clientHca = HostHca(hostLinuxClient, clientInterfaceEth1, clientInterfaceEth2)
    setupObjTuple = (hostLinuxServer, hostLinuxClient, serverHca, clientHca)


# ---------- Start of SomeThread class ------
class SomeThread(threading.Thread):
    def __init__(self, ip):
        try:
            threading.Thread.__init__(self)  # create Thread object
            self.ip = ip
        except:
            raise Exception("Thread fail:" + ip)

    def run(self):
        self.instance = HostLinux(self.ip)
        if self.instance is None:
            self.instance = None


# create HostLinux objects according the inputs, in parallel, and return the list objects to main
def create_objects_in_parallel():
    setup = []
    for host in sys.argv[1:]:  # start from the second cell - first cell contain the script name
        t = SomeThread(host)
        t.start()  # execute the run() def
        setup.append(t)
    for t in setup:
        t.join()  # timeout - Wait until the thread terminates
    print("-----------------------------------------")
    print('-------- All Threads are done! ----------')
    print("-----------------------------------------\n\n")
    return setup
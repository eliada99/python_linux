#!/usr/bin/python
"""
@ By Eliad Avraham - eliada@mellanox.com / eliadush9@gmail.com / +972-525136306
"""
from os import sys, path
import datetime

# My project import
from modules import utilities
from tests import tests
import globals

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


# create new file and save objects details
def save_objects_in_file(setup):
    try:
        file_path = "/.autodirect/QA/qa/smart_nic/AUTOMATION_DO_NOT_DEL/servers_details_" + str(
            datetime.date.today()) + ".txt"
        f = open(file_path, "w+")
    except:
        print("Fail to create the file: " + file_path)
    for host in setup:
        try:
            f.write("Host Name:     %s\r\n" % (str(host.instance.ip)))
            f.write("Ofed Info:    %s\r\n" % (str(host.instance.ofed_info)))
            f.write("MST Version:  %s\r\n" % (str(host.instance.mst_version)))
            f.write("MST Device:   %s\r\n" % (str(host.instance.mst_device)))
            f.write("FW Version:   %s\r\n" % (str(host.instance.fw)))
            f.write("Rom Info:     %s\r\n" % (str(host.instance.exp_rom)))
            f.write("PCI:          %s\r\n" % (str(host.instance.pci)))
            f.write("Board Id:     %s\r\n" % (str(host.instance.board_id)))
            f.write("Part Number:  %s\r\n" % (str(host.instance.part_number)))
            f.write("------------------------------------------\n")
        except:
            # f.write("HostName:     %s\r\n" % (str(host.ip)))
            f.write("Fail to save the content of this host\r\n")
            f.write("------------------------------------------\n")
    print("\r\n------------------------------------------\n")
    utilities.reporter("Check running report in: " + file_path + "\n", 'green')
    print("------------------------------------------\n")
    f.close()


# ---------- Main code ----------
if __name__ == '__main__':
    globals.init()  # create relevant objects and save them in globals module
    DaddyBreakMe = 1

    # verify ping from both ports:
    if (tests.run_ping(globals.hostLinuxClient, globals.serverInterfaceEth1,
                       globals.clientInterfaceEth1, "ipv4") is None):
        noPingIpv4Port_1 = 1
    if (tests.run_ping(globals.hostLinuxClient, globals.serverInterfaceEth2,
                       globals.clientInterfaceEth2, "ipv4") is None):
        noPingIpv4Port_2 = 1

    if (tests.run_ping(globals.hostLinuxClient, globals.serverInterfaceEth1,
                       globals.clientInterfaceEth1, "ipv6") is None):
        noPingIpv6Port_1 = 1
    if (tests.run_ping(globals.hostLinuxClient, globals.serverInterfaceEth2,
                       globals.clientInterfaceEth2, "ipv6") is None):
        noPingIpv6Port_1 = 1

    # verify ping from both ports:
    tests.update_setup_bluefield(globals.hostLinuxServer)
    tests.update_setup_bluefield(globals.hostLinuxClient)

    DaddyBreakMe = 2

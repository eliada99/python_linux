#!/usr/bin/python
# By Eliad Avraham - eliada@mellanox.com
from os import sys, path
import re
import datetime

# My project import
from modules import utilities
import tests
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


# how to..
def usage():
    utilities.reporter("\r\nUsage: ", 'red')
    print("python " + sys.argv[0] + " bfdell01 10.7.15.1")
    utilities.reporter("\r\nYou can run few servers in parallel.\r\nThen save the results in file"
                       " or print the output in your local machine\r\n", 'red')
    exit(2)  # close the app


# ---------- Main code ----------
if __name__ == '__main__':
    if re.findall(r'-h|--help|\?', sys.argv[1]):
        usage()

    globals.init()  # create relevant objects and save them in globals module


    #  WIP - under my debug:
    tests.update_setup_bluefield(globals.hostLinuxServer)
    tests.update_setup_bluefield(globals.hostLinuxClient)


    ##### debug #########
    Daddy = 1

    cmd = "sleep 10"
    out = globals.hostLinuxServer.run_cmd(cmd, "", 1, 20000)
    # utilities.run_cmd - must to send the connection
    output = utilities.run_cmd(globals.objectsList[0].get_conn(), "/sbin/ip link")
    if not output:
        raise Exception("failed to run /sbin/ip link")
    lines = output.split("\n")

    Daddy = 2
    ##### debug #########

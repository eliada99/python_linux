#!/usr/bin/python
import re
import subprocess
import sys
import datetime


# run command RPyC - with/without output
def run_cmd(conn, cmd, output=0):
    if output:
        proc = conn.modules.subprocess.Popen(cmd)
    else:
        proc = conn.modules.subprocess.Popen(cmd, shell=True, stdout=-1, stderr=-1)
    stdout, stderr = proc.communicate()
    if stderr:
        raise Exception("failed to run " + cmd)
        return None
    return stdout


# EXAMPLE: self.ofed_info = utilities.run_cmd_and_regex('ofed_info -s','\w+\-(\d\.\d\-\d\.\d\.\d+\.\d)')
def run_cmd_and_regex(cmd, regex, ret1stOnly=1):
    array = []
    output = run_cmd(cmd).split('\n')
    for line in output:
        # print str(line)+"\n"
        reg = re.findall(regex, line)
        print (reg)
        if reg:
            return reg[0]
        return None


def regex_output(regex, output):
    for line in output:
        reg = re.findall(regex, line)
        if reg:
            return reg
        return None


# Example call: utilities.reporter("Created successfully: " + ip,'green')
def reporter(toPrint, color):
    if color == 'red':
        sys.stdout.write("\033[1;31m")  # print text in red
    elif color == 'green':
        sys.stdout.write("\033[0;32m")  # print text in green
    elif color == 'blue':
        sys.stdout.write("\033[1;34m")  # print text in blue
    elif color == 'bold':
        sys.stdout.write("\033[;1m")  # print text in bold
    print(toPrint)  # print it after add the color to string
    sys.stdout.write("\033[0;0m")  # no colors or formatting - back to the default


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
    reporter("Check running report in: " + file_path + "\n", 'green')
    print("------------------------------------------\n")
    f.close()


def get_current_time():
    start_date = datetime.datetime.now()
    start_date = start_date.strftime("%c")
    start_date = start_date.replace('/', '_')
    start_date = start_date.replace(':', '_')
    start_date = start_date.replace(' ', '_')
    return start_date


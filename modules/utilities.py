#!/usr/bin/python
import re
import sys

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
            #print str(line)+"\n"
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
def reporter(toPrint ,color):
    if   color == 'red':
        sys.stdout.write("\033[1;31m")  # print text in red
    elif color == 'green':
        sys.stdout.write("\033[0;32m")  # print text in green
    elif color == 'blue':
        sys.stdout.write("\033[1;34m")  # print text in blue
    elif color == 'bold':
        sys.stdout.write("\033[;1m")  # print text in bold
    print(toPrint)  # print it after add the color to string
    sys.stdout.write("\033[0;0m")  # no colors or formatting - back to the default
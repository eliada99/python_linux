#!/usr/bin/python
from modules import utilities


# client = Host object
# serverInt = HostInterfaceEth object
# clientInt = HostInterfaceEth object
# ipv = string of "ipv4" or "ipv6"
# count = -c in ping command
def run_ping(client, server_int, client_nt, ipv, count=3):
    if ipv is "ipv4":
        server_ip = server_int.get_ipv4()
        ping = "ping"
    elif ipv is "ipv6":
        server_ip = server_int.get_ipv6()
        ping = "ping6"

    cmd = ping + " -c " + str(count) + " -I " + client_nt.get_interface_name() + " " + server_ip
    try:
        out, err = client.run_cmd(cmd, 0, 1, 1)
        return out, err
    except:
        utilities.reporter("Ping fail: " + cmd + "\n", 'red')
        return False

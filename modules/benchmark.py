#!/usr/bin/python
from modules import utilities

# client = Host object
# serverInt = HostInterfaceEth object
# clientInt = HostInterfaceEth object
# ipv = string of "ipv4" or "ipv6"
def run_ping(client, server_int, client_nt, ipv):
    if ipv is "ipv4":
        server_ip = server_int.get_ipv4()
        ping = "ping"
    elif ipv is "ipv6":
        server_ip = server_int.get_ipv6()
        ping = "ping6"

    cmd = ping + " -c 3 -I " + client_nt.get_interface_name() + " " + server_ip
    try:
        return client.run_cmd(cmd, 0, 1, 1)
    except:
        utilities.reporter("Ping fail: " + cmd + "\n", 'red')
        return None

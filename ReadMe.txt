- Project description:
All objects classes under 'objects' folder.
All modules classes under 'modules' folder.
All tests under 'tests' folder.
Json file - set your setups details.
objects.web2.results - here we save the running results [.html file]

The objects creation start from 'globals.py' - and the access to all objects: [Need to import the globals package]
    globals.<objectName> - For Example:
    tests.update_setup_bluefield(globals.hostLinuxServer)

--------------------------------------------
List of object that created in globals file:
    1. hostLinuxServer
    2. hostLinuxClient
    3. serverInterfaceEth1 = HostInterfaceEth(hostLinuxServer, "eth2") - in hardCoded should be different.
    4. serverInterfaceEth2 = HostInterfaceEth(hostLinuxServer, "eth3")
    5. clientInterfaceEth1 = HostInterfaceEth(hostLinuxClient, "eth4")
    6. clientInterfaceEth2 = HostInterfaceEth(hostLinuxClient, "eth5")
    7. serverHca = HostHca(hostLinuxServer, serverInterfaceEth1, serverInterfaceEth2)
    8. clientHca = HostHca(hostLinuxClient, clientInterfaceEth1, clientInterfaceEth2)
    9. setupObjTuple = (hostLinuxServer, hostLinuxClient, serverHca, clientHca)
--------------------------------------------


Issues:
############### RPyC connection ####################
Pass to connect to hosts via RPyC.
The issue is with my BlueField OS - python 2.7.5 is installed but no RPyC and I cant install it [no access to network].
Started to implement it here:
    RemoteConnection.connect_to_arm()
#################################################
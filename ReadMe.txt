See tha all objects classes in 'objects' folder.
The creation start from 'globals' file - and the access to all objects:
    Need to import the globals package
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

############### RPyC connection ##################################
Pass to connect to hosts via RPyC.
The issue is with my ARM host - python 2.7.5 is installed but no RPyC and I cant install it.
Started to implement it here:
    RemoteConnection.connect_to_arm()
#################################################
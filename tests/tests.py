#!/usr/bin/python
from modules import hostGetData
import globals

VERSIONS_PATH = "../versions.txt"


def update_setup_bluefield(remoteObj):
    myRemoteLocal = globals.hostLinuxServer
    myRemoteLocal = globals.hostLinuxClient
    verDic = hostGetData.get_versions_from_file(VERSIONS_PATH)
    pass
    return
    #remoteObj.run_cmd()
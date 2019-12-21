from rpyc import classic
import rpyc
from modules import sshParamiko, utilities

VER_TOOLS_PATH = '/mswg/projects/ver_tools/reg2_latest/install.sh'
recCounter = 0


class rpycRemoteConnection(object):
    recCounter = 0
    pass

    def connect(self, ip):
        if rpycRemoteConnection.recCounter == 3:
            utilities.reporter("No connection to host: " + ip + "!", 'red')
            return None
        try:
            conn = rpyc.classic.connect(ip)
            return conn
        except Exception as err:
            rpycRemoteConnection.recCounter = rpycRemoteConnection.recCounter + 1
            sshParamiko.ssh_command(str(ip), VER_TOOLS_PATH)
            return self.connect(ip)  # recursion, it is a good day to die

    def async(self, conn_module):
        try:
            res = rpyc.async(conn_module)
            return res
        except Exception as e:
            print e
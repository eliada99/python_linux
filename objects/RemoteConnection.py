"""
@ By Eliad Avraham - eliada@mellanox.com / eliadush9@gmail.com / +972-5136306
"""
import rpyc
from modules import sshParamiko, utilities

VER_TOOLS_PATH = '/mswg/projects/ver_tools/reg2_latest/install.sh'


class RemoteConnection(object):
    pass

    def __init__(self):
        self.recCounter = 0

    def connect(self, ip):
        if self.recCounter == 2:
            utilities.reporter("No connection to host: " + ip + "!", 'red')
            return None
        try:
            conn = rpyc.classic.connect(ip)
            return conn
        except Exception as err:
            self.recCounter += 1
            utilities.reporter("No connection to host: " + ip + " via RPyC service.\n" +
                               "starting to install the ver_tools: " + VER_TOOLS_PATH, 'yellow')
            sshParamiko.ssh_command(str(ip), VER_TOOLS_PATH)
            return self.connect(ip)  # recursion, it is a good day to die

    def connect_to_arm(self, ip):
        pass
        '''
        The problem with bluefield connection is that you dont have access to /mswg/ and you cant install
        # nothing via 'yum install' due to repos issue.
        # after resolve this, you can try the 'tunneling' feature of RPyC.

        #conn = rpyc.classic.connect(ip)
        #sock = conn.modules.socket.socket()
        #sock.connect(("192.168.100.2", 80))

        #sock.send("cat /etc/mlnx-release")
        #sock.recv()
        '''

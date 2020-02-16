import Paramiko
import time


class SshConnection(object):
    vla1 = 1

    def __init__(self, ip, user, password):
        self.ssh = None
        self.ip = str(ip)
        self.user = user
        self.password = password

    def connect(self):
        print("connecting to device " + self.ip + " via ssh connection [Paramiko]")
        self.ssh = Paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(Paramiko.AutoAddPolicy())

        try:
            self.ssh.connect(
                str(self.ip),
                port=22,
                username=self.user,
                password=self.password,
                look_for_keys=False,
                allow_agent=False,
                timeout=5
            )

        except Exception:
            var = self.ip, "error : ssh connection failed"
            print("error :: " + str(var))
            raise Exception

        print(str(self.ip) + " is connecting")
        return self

    def send(self, command, timeout=None):
        stdin, stdout, stderr = self.ssh.exec_command(str(command), timeout=timeout)
        time.sleep(1.0)
        output = stdout.readlines()
        print(stdout.read())
        print('\n'.join(output))
        return output

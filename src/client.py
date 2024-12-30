from paramiko import SSHClient, AutoAddPolicy, Ed25519Key, Transport, SFTPClient


COMMAND = "apt --version"
HOST = "3.110.175.222"
local_file = "/home/ncs/opt/workspace/vortexdude/PortCraft/"
remote_file = "/home/ubuntu/PortCraft"

class SSH:
    def __init__(self, host, user, key=None, port=22):
        self.port = port
        self.user = user
        self.host = host
        self.pkey = Ed25519Key.from_private_key_file(filename=key)
        self._client = self.key_based_connect()
        self._sftp_client = self._sftp_client_connect()

    @classmethod
    def default(cls, host):
        user = "ubuntu"
        key = "/home/ncs/.ssh/butena.pem"
        return cls(
            host=host,
            user=user,
            key=key
        )

    @property
    def client(self):
        return self._client

    @property
    def sftp_client(self):
        return self._sftp_client

    def key_based_connect(self):
        _client = SSHClient()
        _policy = AutoAddPolicy()
        _client.set_missing_host_key_policy(_policy)
        _client.connect(self.host, username=self.user, pkey=self.pkey)
        return _client

    def exec_command(self, command) -> tuple:
        _stdin, _stdout, _stderr = self.client.exec_command(command)
        return _stdin, _stdout, _stderr

    def _sftp_client_connect(self):
        transport = Transport((self.host, self.port))
        transport.connect(username=self.user, pkey=self.pkey)
        return SFTPClient.from_transport(transport)

    def get_file(self, local_path, remote_path):
        return self.sftp_client.get(remote_path,local_path)

    def put_file(self, local_file, remote_file):
        return self.sftp_client.put(local_file, remote_file)

client = SSH.default(host=HOST)
client.put_file(local_file, remote_file)

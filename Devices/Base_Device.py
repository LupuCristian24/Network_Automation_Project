from Connection import SSHConnection


class NetworkDevice:
    """
    Base class for network devices.
    """

    def __init__(self, hostname, ip_address, username, password, enable_password):
        self.hostname = hostname
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.enable_password = enable_password
        # self.connection = SSHConnection(ip_address, username, password)
        self.connection = SSHConnection(self)

    def connect(self):
        """
        Establish SSH connection to the device.
        """
        self.connection.connect()

    def execute_command(self, command):
        """
        Execute a command on the device via SSH.
        """
        stdout, stderr = self.connection.send_command(command)
        if stderr:
            raise Exception(f"Error executing command '{command}': {stderr}")
        return stdout

    def disconnect(self):
        """
        Close the SSH connection.
        """
        self.connection.close()
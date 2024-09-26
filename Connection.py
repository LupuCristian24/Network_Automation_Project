import paramiko
from multiprocessing import Lock
from time import sleep


class SSHConnection:
    """
    Connection Class
    """

    _instances = {}
    _lock = Lock()

    def __new__(cls, device):
        # Acquire the lock before modifying class variables
        with cls._lock:
            # Check if an instance already exists for the device
            if device.hostname not in cls._instances:
                # Create a new instance if it doesn't exist
                cls._instances[device.hostname] = super(SSHConnection, cls).__new__(cls)
        return cls._instances[device.hostname]

    def __init__(self, device):
        if not hasattr(self, 'client'):  # Prevent __init__ from running multiple times for the same device
            self.ip_address = device.ip_address
            self.username = device.username
            self.password = device.password
            self.device = device
            self.client = None
            self.shell = None

    def connect(self, en_pass) -> None:
        """
        Method that establishes the SSH connection to the device.
        """
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.ip_address, username=self.username, password=self.password)
            self.shell = self.client.invoke_shell()
            self.shell.send(f'en\n{en_pass}\nconf t\n')
            sleep(3)
        except paramiko.SSHException as e:
            print(f"Failed to connect to {self.ip_address}: {e}")
            self.close()

    def send_command(self, command):
        """
        Method that sends the command to the device.
        """
        # stdin, stdout, stderr = self.client.exec_command(command)
        # return stdout.read().decode(), stderr.read().decode()

        if not self.shell:
            print("Connection not established. Please connect first.")
            return None, "Connection not established."
        self.shell.send(command + '\n')
        sleep(3)
        output = ""
        while self.shell.recv_ready():
            output += self.shell.recv(65535).decode('utf-8')
        return output, ""

    def close(self) -> None:
        """
        Method that closes the SSH connection.
        """
        if self.client:
            self.client.close()
            self.client = None
            self.shell = None
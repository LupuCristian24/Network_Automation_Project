from Devices.Base_Device import NetworkDevice
import subprocess
from time import sleep


class Switch(NetworkDevice):
    """
    Class representing a network switch.
    """

    def configure_vlans(self, vlans):
        """
        Configure VLANs on the switch.
        """
        self.connection.connect(self)
        commands = []
        for vlan_id in vlans:
            sleep(1)
            commands.extend([
                f'vlan {vlan_id}',
                f'name Vlan{vlan_id}',
                'exit'
            ])
        try:
            for cmd in commands:
                self.execute_command(cmd)
            print("\nVlans created successfully.")
        except Exception as error:
            print(f"Error occurred during VLAN configuration: {error}")
        finally:
            self.connection.close()

    def configure_port_security(self, max_mac_addresses=1):
        """
        Configure port security on interfaces.
        """
        self.connection.connect(self)
        try:
            while True:
                interface = input("Enter the interface you want to configure (ex: gi0/1): ")
                commands = [
                    f'interface {interface}',
                    'switchport mode access',
                    'switchport port-security',
                    'switchport port-security maximum 20',
                    'switchport port-security violation shutdown',
                    'exit'
                ]
                for cmd in commands:
                    self.execute_command(cmd)
                print(f"\nPort security configured successfully on {interface}.")

                add_another = input("Do you want to configure port security on another interface? (yes/no): ")
                if add_another.lower() != 'yes':
                    break
        except Exception as error:
            print(f"Error occurred during port security configuration: {error}")
        finally:
            self.connection.close()

    def configure_rstp(self):
        """
        Configure RSTP security features.
        """
        self.connection.connect(self)
        commands = [
            'spanning-tree mode rapid-pvst',
        ]
        try:
            for cmd in commands:
                self.execute_command(cmd)
            print("\nRSTP configured successfully.")
        except Exception as error:
            print(f"Error occurred during RSTP configuration: {error}")
        finally:
            self.connection.close()

    def configure_stp_security(self):
        """
        Configure STP security on user-specified interfaces.
        """
        self.connection.connect(self)
        try:
            while True:
                interface = input("Enter the interface you want to configure (ex: gi0/1): ")
                commands = [
                    f'interface {interface}',
                    'spanning-tree portfast',
                    'spanning-tree portfast edge bpduguard default',
                    'exit'
                ]
                for cmd in commands:
                    self.execute_command(cmd)
                print(f"\nSTP configured successfully on {interface}.")

                add_another = input("Do you want to configure STP security on another interface? (yes/no): ")
                if add_another.lower() != 'yes':
                    break
        except Exception as error:
            print(f"Error occurred during STP configuration: {error}")
        finally:
            self.connection.close()

    def configure_hsrp(self):
        """
        Configure HSRP on an interface.
        """
        self.connection.connect(self)
        interface = input('Enter the interface name (ex: gi0/0): ')
        group = input('Enter the HSRP group name: ')
        virtual_ip = input('Enter the HSRP virtual ip address: ')
        priority = input('Enter the HSRP priority or None: ')

        true_priority = "100" if priority == "None" else int(priority)

        commands = [
            f'interface {interface}',
            f'standby {group} ip {virtual_ip}',
            f'standby {group} preempt',
            f'standby {group} priority {true_priority}',
            'exit'
        ]
        try:
            for cmd in commands:
                self.connection.send_command(cmd)
            print("\nHSRP configured successfully.")
        except Exception as error:
            print(f"Error occurred during HSRP configuration: {error}")
        finally:
            self.connection.close()

    def ping_device(self):
        """
        Send a ping from the router to another device specified by the user and display whether the ping was successful.
        """
        target_ip = input("Enter the IP address of the target device to ping: ")
        try:
            self.connection.connect(self.enable_password)
            # Execute the ping command via subprocess
            command = ["ping", "-c", "4", target_ip]
            ping_result = subprocess.run(command, capture_output=True, text=True)
            # Check the return code to determine the success of the ping
            connectivity_status = "successful" if ping_result.returncode == 0 else "failed"
            if connectivity_status == "successful":
                print(f"\nPing to {target_ip} was successful! Connectivity is established.")
            else:
                print(f"\nPing to {target_ip} failed. No connectivity detected.")
        except Exception as error:
            print(f"Error occurred during ping operation: {error}")
        finally:
            self.connection.close()

    def save_config(self):
        """
        Save the running configuration to startup configuration.
        """
        try:
            self.connection.connect(self)
            stdout, stderr = self.connection.send_command("do wr")
            if stderr:
                print(f"\nError saving configuration: {stderr}")
            else:
                print("\nConfiguration saved successfully.")
        except Exception as e:
            print(f"\nAn error occurred while saving the configuration: {e}")
        finally:
            self.connection.close()

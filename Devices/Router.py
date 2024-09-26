from Devices.Base_Device import NetworkDevice
import subprocess


class Router(NetworkDevice):
    """
    Represents a network router, extending NetworkDevice with methods for configuration.
    """

    def configure_interfaces(self, interfaces):
        """
        Configure interfaces with IP addresses. Asks the user if they want to enter manual configuration.
        If not, uses the default values provided in the `interfaces` parameter.
        """
        manual_config = input("Do you want to configure the interfaces manually? (yes/no): ")
        if manual_config == 'yes':
            interfaces_list = {}
            while True:
                interface = input("Enter the interface (e.g., GigabitEthernet0/0): ")
                ip_address = input("Enter the IP address and mask address (ex: {ip} {mask}): ")

                interfaces_list[interface] = f'{ip_address}'
                another = input("Do you want to add another interface? (yes/no): ")
                if another != 'yes':
                    break
        else:
            interfaces_list = interfaces
        try:
            self.connection.connect(self)
            for interface, ip in interfaces_list.items():
                commands = [
                    f'interface {interface}',
                    f'ip address {ip}',
                    'no shutdown',
                    'exit'
                ]
                for cmd in commands:
                    self.connection.send_command(cmd)
            print("\nRouter IP configuration done.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
        finally:
            self.connection.close()

    def configure_ripV2(self):
        """
        Configures RipV2 on router by automatically detecting directly connected networks (C routes).
        """
        self.connection.connect(self)
        stdout, stderr = self.connection.send_command("do show ip route")
        if stderr:
            print(f"Error retrieving routing table: {stderr}")
            self.connection.close()
            return
        connected_networks = []
        for line in stdout.splitlines():
            if line.startswith("C"):
                parts = line.split()
                if len(parts) > 1 and "/" in parts[1]:
                    network = parts[1].split('/')[0]
                    connected_networks.append(network)
        commands = [
            "router rip",
            "version 2",
            "no auto-summary",
        ]
        for network in connected_networks:
            commands.append(f'network {network}')
        commands.append('exit')
        for command in commands:
            stdout, stderr = self.connection.send_command(command)
            if stderr:
                print(f"Error executing command {command}: {stderr}")
            else:
                print(f"Executed: {command}")
        print("\nRouter ripV2 configuration done.")
        self.connection.close()

    def configure_static_routes(self):
        """
        Configures Static Routes on the router's interface based on user input.
        Format for input: <destination network> <subnet mask> <next-hop IP>
        Example input: '0.0.0.0 0.0.0.0 192.168.1.1, 10.1.1.0 255.255.255.0 192.168.2.1'
        """
        self.connection.connect(self)
        routes = input('Enter the static routes separated by comma (ex: 0.0.0.0 0.0.0.0 192.168.1.1,'
                       ' 10.1.1.0 255.255.255.0 192.168.2.1): ')
        static_routes_list = routes.split(',')
        static_routes = []

        for route in static_routes_list:
            route = route.strip()
            route_parts = route.split()
            if len(route_parts) != 3:
                print(f"Invalid format for route: {route}. Expected format: <network> <subnet mask> <next-hop IP>")
                continue
            destination_network, subnet_mask, next_hop = route_parts
            static_routes.append((destination_network, subnet_mask, next_hop))
        if not static_routes:
            print("No valid static routes provided.")
            return
        commands = []
        for destination_network, subnet_mask, next_hop in static_routes:
            command = f"ip route {destination_network} {subnet_mask} {next_hop}"
            commands.append(command)
        commands.append('exit')
        for cmd in commands:
            self.connection.send_command(cmd)
        print("\nStatic routes configuration complete.")
        self.connection.close()

    def configure_hsrp(self):
        """
        Configure HSRP on an interface, asks for interface, group id, virtual ip address and priority number (optional).
        """
        self.connection.connect(self)
        interface = input('Enter the interface name (ex: gi0/0): ')
        group = input('Enter the HSRP group name: ')
        virtual_ip = input('Enter the HSRP virtual ip address: ')
        priority = input('Enter the HSRP priority or None: ')

        if priority == "None":
            true_priority = "100"
        else:
            true_priority = int(priority)

        commands = [
            f'interface {interface}',
            'standby version 2'
            f'standby {group} ip {virtual_ip}',
            f'standby {group} preempt',
            f'standby {group} priority {true_priority}',
            'exit'
        ]
        for cmd in commands:
            self.connection.send_command(cmd)
        print("\nHSRP configuration completed successfully.")
        self.connection.close()

    def configure_dhcp_pool(self):
        """
        Configure a DHCP pool on the router based on user input.
        This will configure the pool name, network, default router, DNS server (optional),
        and optionally exclude IP addresses.
        """
        self.connection.connect(self)
        pool_name = input("Enter the pool name: ")
        network = input("Enter the network address ({ip_address} {mask_address}): ")
        default_router = input("Enter the default router address: ")
        dns_server = input("Enter the DNS server address or None: ")
        exclude_addresses = input("Enter the excluded addresses separated by a comma or type None: ")
        if not pool_name or not network or not default_router:
            print("Pool name, network address, and default router are required.")
        commands = [
            f'ip dhcp pool {pool_name}',
            f'network {network}',
            f'default-router {default_router}',
        ]
        if exclude_addresses.strip():
            exclude_list = exclude_addresses.split(',')
            for addr in exclude_list:
                addr = addr.strip()
                commands.insert(0, f'ip dhcp excluded-address {addr}')
        if dns_server != "None" and dns_server.strip():
            commands.append(f'dns-server {dns_server}')
        commands.append('exit')
        for cmd in commands:
            self.connection.send_command(cmd)
        print("\nDHCP pool configuration completed successfully.")
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


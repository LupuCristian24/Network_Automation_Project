from Devices.Switch import Switch
from Devices.Router import Router
import json


def load_device_data(filename):
    """
    Loads data from JSON file.
    """
    with open(filename) as file:
        return json.load(file)


def display_main_menu() -> None:
    """Display the main menu options."""
    print("""
Welcome to the Network Automation Tool!

You have the following options available:
    1. Configure a device.
    2. Exit the application.
    """)


def find_device(devices: list, ip_address: str):
    """Searches for a device by IP address in the list of devices."""
    for device in devices:
        if device['ip_address'] == ip_address:
            return device
    return None


def configure_device(device: dict) -> None:
    """Configures the device based on its type."""
    if device['type'].lower() == 'router':
        ConfigMenuRouter(device)
    elif device['type'].lower() == 'switch':
        ConfigMenuSwitch(device)


def main() -> None:
    """Main function to execute the primary routine."""
    devices = load_device_data('devices_config.json')
    routers = devices.get('routers', [])
    switches = devices.get('switches', [])

    while True:
        display_main_menu()
        choice = input("Please enter your choice: ")

        if choice == '1':
            target_device_ip = input("Enter the IP address of the device you wish to configure: ")
            device = find_device(routers, target_device_ip) or find_device(switches, target_device_ip)
            if device:
                configure_device(device)
            else:
                print("The specified device was not found. Please enter a valid IP address.")
        elif choice == '2':
            print("Thank you for using the Network Automation Tool. Goodbye!")
            exit()
        else:
            print("Invalid selection. Please choose either 1 or 2.")


def ConfigMenuRouter(device: dict) -> None:
    """Menu with configuration options for Router."""
    router_instance = Router(device['hostname'], device['ip_address'], device['username'],
                             device['password'], device['enable_password'])

    while True:
        print(f"\nConfiguring Router: {device['hostname']} ({device['ip_address']})")
        print("""
The following configuration options are available for the Router:
    1. Configure a sub-interface.
    2. Set up a DHCP Server.
    3. Configure HSRP.
    4. Enable ripV2.
    5. Configure Static Routes.
    6. Verify Connectivity
    7. Save Configuration
    8. Return to Main Menu.
        """)

        config_choice = input("Please enter your choice: ")

        if config_choice == '1':
            router_instance.configure_interfaces(device['interfaces'])
        elif config_choice == '2':
            router_instance.configure_dhcp_pool()
        elif config_choice == '3':
            router_instance.configure_hsrp()
        elif config_choice == '4':
            router_instance.configure_ripV2()
        elif config_choice == '5':
            router_instance.configure_static_routes()
        elif config_choice == '6':
            router_instance.ping_device()
        elif config_choice == '7':
            router_instance.save_config()
        elif config_choice == '8':
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid option. Please select a valid choice.")


def ConfigMenuSwitch(device: dict) -> None:
    """Menu with configuration options for Switch."""
    switch_instance = Switch(device['hostname'], device['ip_address'], device['username'],
                             device['password'], device['enable_password'])

    while True:
        print(f"\nConfiguring Switch: {device['hostname']} ({device['ip_address']})")
        print("""
The following configuration options are available for the Switch:
    1. Configure a VLAN.
    2. Set up Port Security.
    3. Enable RSTP.
    4. Configure STP.
    5. Configure HSRP (for multilayer switches only).
    6. Verify Connectivity
    7. Save Configuration
    8. Return to Main Menu.
        """)

        config_choice = input("Please enter your choice: ")

        if config_choice == '1':
            switch_instance.configure_vlans(device['vlans'])
        elif config_choice == '2':
            switch_instance.configure_port_security()
        elif config_choice == '3':
            switch_instance.configure_rstp()
        elif config_choice == '4':
            switch_instance.configure_stp_security()
        elif config_choice == '5':
            if "multilayer" not in device['type'].lower():
                print("\nnThis is not a multilayer switch!")
            else:
                switch_instance.configure_hsrp()
        elif config_choice == '6':
            switch_instance.ping_device()
        elif config_choice == '7':
            switch_instance.save_config()
        elif config_choice == '8':
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid option. Please select a valid choice.")

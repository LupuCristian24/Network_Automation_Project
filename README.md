# Network Automation Tool

Welcome to the **Network Automation Tool**! This tool is designed to assist network administrators in configuring and managing network devices such as routers and switches via an interactive command-line interface. It simplifies common configuration tasks like setting up VLANs, configuring DHCP, or routing protocols such as RIP, HSRP, and static routes.

## Features
- **Configure Routers**: Options for configuring interfaces, DHCP pools, RIP version 2, HSRP, and static routes.
- **Configure Switches**: Options for setting up VLANs, port security, RSTP, STP security, and HSRP for multilayer switches.
- **SSH Connectivity**: Securely connect to devices over SSH to execute commands.
- **Device Inventory**: Pre-defined devices (routers and switches) available in the `devices_config.json` file for quick selection and configuration.

## File Structure

```
- Devices/
  - Router.py        # Router class to manage router configurations
  - Switch.py        # Switch class to manage switch configurations
  - Base_Device.py   # Base class for network devices
- Connection.py      # SSH connection management using Paramiko
- devices_config.json # JSON file with predefined router and switch configurations
- main.py            # The main script that starts the application
- Menu.py            # Menu class to allow the user to interact with the tool
- requirements.txt   # Lists the dependencies required for the project
```

### Dependencies
- `paramiko`: Used for SSH connection handling.
- `json`: For reading device configuration files.

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/network-automation-tool.git
   cd network-automation-tool
   ```

2. Install dependencies:
   ```bash
   pip install paramiko
   ```

3. Make sure your device configurations are properly set up in `devices_config.json`.

### Usage

Run the application with the following command:

```bash
python3 main.py
```

The main menu will guide you through the available options:

1. **Configure a Device**:
   - Enter the IP address of the device.
   - Configure routers or switches with detailed sub-menus for specific tasks (e.g., DHCP, VLANs, RIP, HSRP, etc.).

2. **Exit the Application**:
   - Exits the tool.

### Example Device Configurations (in `devices_config.json`)

```json
{
  "routers": [
    {
      "hostname": "R4",
      "type": "router",
      "ip_address": "192.168.1.2",
      "interfaces": {
        "GigabitEthernet0/0": "192.168.1.2 255.255.255.0",
        "GigabitEthernet0/1": "10.10.20.1 255.255.255.0"
      },
      "username": "admin",
      "password": "cisco",
      "enable_password": "pass"
    }
  ],
  "switches": [
    {
      "hostname": "SW4",
      "type": "switch",
      "ip_address": "192.168.1.254",
      "vlans": [10, 20],
      "interfaces": ["GigabitEthernet0/0", "GigabitEthernet0/1", "GigabitEthernet0/2"],
      "username": "admin",
      "password": "cisco",
      "enable_password": "pass"
    }
  ]
}
```

### How to Add a New Device

1. Open `devices_config.json`.
2. Add a new entry under the appropriate section (either `routers` or `switches`), specifying details like `hostname`, `type`, `ip_address`, `interfaces`, etc.
3. Save the file, and the device will be available for configuration in the tool.

### Available Device Configuration Options

#### Router Configuration
- **Configure Sub-interfaces**
- **Set up DHCP Server**
- **Enable RIP version 2**
- **Configure Static Routes**
- **Enable HSRP**
- **Verify Connectivity**

#### Switch Configuration
- **Configure VLANs**
- **Set up Port Security**
- **Enable RSTP**
- **Configure STP Security**
- **Enable HSRP for Multilayer Switches**
- **Verify Connectivity**


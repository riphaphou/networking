# Network Simulator - Similar to Cisco Packet Tracer

A network simulation tool that allows you to create, configure, and test network topologies. Similar to Cisco Packet Tracer, this tool provides both a graphical interface and a command-line interface for network design and testing.

## Features

- 🖥️ **Network Devices**: Create computers, routers, and switches
- 🔧 **IP Configuration**: Configure IP addresses and subnet masks on network interfaces
- 🌐 **Gateway Setup**: Set default gateways for routing between networks
- 🔗 **Device Connections**: Connect devices via network interfaces
- 📡 **Ping Testing**: Test network connectivity with ping simulation
- 🎨 **Graphical Interface**: Visual network topology designer (GUI mode)
- ⌨️ **Command-Line Interface**: Full-featured CLI for network configuration
- 📊 **Network Information**: View detailed device and topology information

## Installation

This project uses only Python standard library, so no additional dependencies are required!

```bash
# Clone the repository
git clone https://github.com/riphaphou/networking.git
cd networking

# No pip install needed - uses Python standard library only!
```

## Usage

### GUI Mode (Default)

Start the graphical interface:

```bash
python main.py
# or
python main.py --gui
```

#### GUI Features:
- **Add Devices**: Click on "➕ Computer", "➕ Router", or "➕ Switch" to add devices
- **Configure IP**: Click "🔧 Configure IP" to set IP addresses
- **Set Gateway**: Click "🌐 Set Gateway" to configure default gateways
- **Connect Devices**: Click "🔗 Connect" to link devices together
- **Ping Test**: Click "📡 Ping" to test connectivity
- **Device Info**: Click "ℹ️ Info" to view device details
- **Drag & Drop**: Click and drag devices to rearrange the topology

### CLI Mode

Start the command-line interface:

```bash
python main.py --cli
```

#### CLI Commands:

```
add_computer <name>              - Add a computer to the network
add_router <name>                - Add a router to the network
add_switch <name>                - Add a switch to the network
configure_ip <device> <interface> <ip> [mask] - Configure IP address
set_gateway <computer> <gateway_ip>  - Set default gateway
connect <dev1> <int1> <dev2> <int2>  - Connect two devices
ping <computer> <target_ip>      - Ping from a computer to target IP
show_topology                    - Display network topology
show_device <device_name>        - Show device details
list                            - List all devices
help                            - Show help message
exit/quit                       - Exit the simulator
```

## Examples

### Example 1: Simple Network (CLI)

```bash
python main.py --cli
```

Then in the CLI:
```
NetSim> add_computer PC1
NetSim> add_computer PC2
NetSim> configure_ip PC1 eth0 192.168.1.10
NetSim> configure_ip PC2 eth0 192.168.1.20
NetSim> connect PC1 eth0 PC2 eth0
NetSim> ping PC1 192.168.1.20
NetSim> show_topology
```

### Example 2: Network with Router (CLI)

```
NetSim> add_computer PC1
NetSim> add_computer PC2
NetSim> add_router R1
NetSim> configure_ip PC1 eth0 192.168.1.10
NetSim> configure_ip PC2 eth0 192.168.2.10
NetSim> configure_ip R1 eth0 192.168.1.1
NetSim> configure_ip R1 eth1 192.168.2.1
NetSim> connect PC1 eth0 R1 eth0
NetSim> connect PC2 eth0 R1 eth1
NetSim> set_gateway PC1 192.168.1.1
NetSim> set_gateway PC2 192.168.2.1
NetSim> ping PC1 192.168.2.10
```

### Example 3: Using the GUI

1. Run `python main.py`
2. Click "➕ Computer" twice to add PC1 and PC2
3. Click "🔧 Configure IP" and set:
   - PC1 eth0: 192.168.1.10
   - PC2 eth0: 192.168.1.20
4. Click "🔗 Connect" to connect PC1:eth0 to PC2:eth0
5. Click "📡 Ping" and ping from PC1 to 192.168.1.20
6. See the result in the dialog box!

## Architecture

### Core Components

- **`network_device.py`**: Device classes (Computer, Router, Switch, NetworkInterface)
- **`network_topology.py`**: Topology management and device connections
- **`network_cli.py`**: Command-line interface
- **`network_gui.py`**: Graphical user interface
- **`main.py`**: Application entry point

### Device Types

1. **Computer**: End-user device with network interface and gateway support
2. **Router**: Multi-interface device for routing between networks
3. **Switch**: Layer 2 device for connecting multiple devices

### Network Simulation

The simulator implements:
- IP address validation and configuration
- Subnet mask handling
- Same-network detection
- Gateway-based routing
- Ping simulation with hop tracking

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)

## Platform Support

- ✅ Linux
- ✅ macOS
- ✅ Windows

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## License

This project is open source and available for educational purposes.

## Screenshots

### GUI Mode
The GUI provides a visual canvas where you can:
- Drag and drop network devices
- See connections between devices
- Configure devices with dialog boxes
- View network information in real-time

### CLI Mode
The CLI provides a powerful command-line interface for:
- Scripting network configurations
- Batch operations
- Learning networking concepts
- Quick testing scenarios

## Future Enhancements

Potential features for future versions:
- Save/load network topologies
- More network protocols (ARP, DHCP, etc.)
- Packet capture simulation
- Advanced routing protocols (RIP, OSPF)
- VLANs and trunk ports
- Network analysis tools
- Export topology diagrams

## Contact

For questions or support, please open an issue on GitHub.
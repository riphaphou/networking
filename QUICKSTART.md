# Quick Start Guide

## Installation

```bash
git clone https://github.com/riphaphou/networking.git
cd networking
```

No dependencies to install - uses Python standard library only!

## 5-Minute Tutorial

### Option 1: GUI Mode (Visual)

```bash
python main.py
```

1. Click "➕ Computer" → Enter "PC1"
2. Click "➕ Computer" → Enter "PC2"
3. Click "🔧 Configure IP":
   - Device: PC1, Interface: eth0, IP: 192.168.1.10
   - Click Apply
4. Click "🔧 Configure IP":
   - Device: PC2, Interface: eth0, IP: 192.168.1.20
   - Click Apply
5. Click "🔗 Connect":
   - Device 1: PC1, Interface 1: eth0
   - Device 2: PC2, Interface 2: eth0
   - Click Connect
6. Click "📡 Ping":
   - Source: PC1, Target IP: 192.168.1.20
   - Click Ping
7. See success message! ✓

### Option 2: CLI Mode (Command Line)

```bash
python main.py --cli
```

Then type these commands:

```
add_computer PC1
add_computer PC2
configure_ip PC1 eth0 192.168.1.10
configure_ip PC2 eth0 192.168.1.20
connect PC1 eth0 PC2 eth0
ping PC1 192.168.1.20
show_topology
```

### Option 3: Run Examples

Simple network:
```bash
python example1_simple_network.py
```

Router with two subnets:
```bash
python example2_router_network.py
```

Switched network:
```bash
python example3_switch_network.py
```

## Common Tasks

### Create a Network with Router

```python
# In Python or use CLI commands
from network_topology import NetworkTopology

topology = NetworkTopology()

# Add devices
pc1 = topology.add_computer("PC1")
pc2 = topology.add_computer("PC2")
router = topology.add_router("R1")

# Configure Network 1 (192.168.1.0/24)
pc1.configure_interface("eth0", "192.168.1.10")
router.configure_interface("eth0", "192.168.1.1")

# Configure Network 2 (192.168.2.0/24)
pc2.configure_interface("eth0", "192.168.2.10")
router.configure_interface("eth1", "192.168.2.1")

# Set gateways
pc1.set_default_gateway("192.168.1.1")
pc2.set_default_gateway("192.168.2.1")

# Connect devices
topology.connect_devices("PC1", "eth0", "R1", "eth0")
topology.connect_devices("PC2", "eth0", "R1", "eth1")

# Test connectivity
result = pc1.ping("192.168.2.10", topology)
print(result)  # Success! Path: PC1 -> R1 -> PC2
```

### CLI Commands Reference

```
add_computer <name>                          Add a computer
add_router <name>                            Add a router
add_switch <name>                            Add a switch
configure_ip <device> <interface> <ip> [mask] Configure IP
set_gateway <computer> <gateway_ip>          Set gateway
connect <dev1> <int1> <dev2> <int2>         Connect devices
ping <computer> <target_ip>                  Test connectivity
show_topology                                View network
show_device <name>                           View device info
list                                         List all devices
help                                         Show all commands
exit                                         Quit
```

## Learning Resources

- See `README.md` for full documentation
- See `GUI_GUIDE.md` for GUI usage details
- See `example*.py` files for code examples
- Run `python test_network_simulator.py` to see how it works

## Need Help?

1. Type `help` in the CLI for all commands
2. Check the README.md for detailed documentation
3. Run the example scripts to see working configurations
4. All code is well-commented - read the source!

## Next Steps

- Create more complex topologies
- Experiment with different subnet masks
- Try multi-hop routing scenarios
- Build your own network designs

Have fun learning networking! 🚀

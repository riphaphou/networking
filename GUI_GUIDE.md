# GUI Screenshots and Usage Guide

## Network Simulator GUI

### Main Interface

The GUI provides an intuitive interface similar to Cisco Packet Tracer with the following components:

#### Toolbar (Top)
- **➕ Computer**: Add a computer to the network
- **➕ Router**: Add a router to the network
- **➕ Switch**: Add a switch to the network
- **🔧 Configure IP**: Configure IP addresses on devices
- **🌐 Set Gateway**: Set default gateway for computers
- **🔗 Connect**: Connect two devices together
- **📡 Ping**: Test network connectivity
- **ℹ️ Info**: View detailed device information

#### Canvas (Center)
- Visual representation of network devices
- Drag and drop devices to rearrange the topology
- Visual connections shown as blue dashed lines between devices
- Device icons:
  - 💻 Computers (Green)
  - 🔀 Routers (Blue)
  - ⚡ Switches (Orange)

#### Information Panel (Right)
- Real-time display of all devices in the network
- Shows IP addresses configured on each device
- Shows gateway information for computers
- Automatically updates when changes are made

### Sample Workflow

1. **Creating a Simple Network**
   - Click "➕ Computer" and enter "PC1"
   - Click "➕ Computer" and enter "PC2"
   - Devices appear on the canvas

2. **Configuring IP Addresses**
   - Click "🔧 Configure IP"
   - Select device: PC1
   - Interface: eth0
   - IP Address: 192.168.1.10
   - Subnet Mask: 255.255.255.0
   - Click "Apply"
   - Repeat for PC2 with IP 192.168.1.20

3. **Connecting Devices**
   - Click "🔗 Connect"
   - Device 1: PC1, Interface 1: eth0
   - Device 2: PC2, Interface 2: eth0
   - Click "Connect"
   - Blue dashed line appears between devices

4. **Testing Connectivity**
   - Click "📡 Ping"
   - Source Computer: PC1
   - Target IP: 192.168.1.20
   - Click "Ping"
   - Result dialog shows:
     * Status: SUCCESS ✓
     * Message: Reply from 192.168.1.20: bytes=32 time<1ms TTL=64
     * Path: PC1 -> PC2

### Features

#### Interactive Canvas
- **Drag and Drop**: Click and drag any device to reposition it
- **Auto-Redraw**: Connections automatically update when devices move
- **Visual Feedback**: Devices are color-coded by type

#### Configuration Dialogs
All configuration operations use clear dialog boxes:
- Dropdown menus for selecting devices
- Text fields for entering IP addresses
- Default values pre-filled (e.g., 255.255.255.0 for subnet mask)
- Validation with error messages for invalid inputs

#### Information Display
The right panel shows:
```
Total Devices: 3

━━━ PC1 (Computer) ━━━
  eth0: 192.168.1.10
  Gateway: 192.168.1.1

━━━ R1 (Router) ━━━
  eth0: 192.168.1.1
  eth1: 192.168.2.1

━━━ PC2 (Computer) ━━━
  eth0: 192.168.2.10
  Gateway: 192.168.2.1
```

### Advanced Features

#### Multi-Network Setup
1. Add PC1, PC2, and Router R1
2. Configure:
   - PC1: 192.168.1.10 (Network 1)
   - R1 eth0: 192.168.1.1 (Network 1)
   - R1 eth1: 192.168.2.1 (Network 2)
   - PC2: 192.168.2.10 (Network 2)
3. Set gateways:
   - PC1 gateway: 192.168.1.1
   - PC2 gateway: 192.168.2.1
4. Connect:
   - PC1:eth0 to R1:eth0
   - PC2:eth0 to R1:eth1
5. Ping from PC1 to 192.168.2.10
   - Result shows path: PC1 -> R1 -> PC2

#### Switch Networks
1. Add PC1, PC2, PC3, and Switch SW1
2. Configure all PCs on same network (192.168.1.0/24)
3. Connect all PCs to different switch ports
4. Test connectivity between any two PCs
5. All communication goes through the switch

### Running the GUI

```bash
# Start GUI mode (default)
python main.py

# Or explicitly specify GUI mode
python main.py --gui
```

### System Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)
- Works on Windows, macOS, and Linux

### Troubleshooting

If the GUI doesn't start:
1. Check if tkinter is installed:
   ```bash
   python -c "import tkinter"
   ```
2. On Ubuntu/Debian, install with:
   ```bash
   sudo apt-get install python3-tk
   ```
3. On macOS with Homebrew:
   ```bash
   brew install python-tk
   ```
4. Alternatively, use CLI mode:
   ```bash
   python main.py --cli
   ```

"""Network topology management for the simulation tool."""

from typing import Dict, List, Optional, Tuple
from network_device import NetworkDevice, Computer, Router, Switch, NetworkInterface


class NetworkTopology:
    """Manages the network topology and connections."""
    
    def __init__(self):
        self.devices: Dict[str, NetworkDevice] = {}
        self.connections: List[Tuple[str, str]] = []  # List of (device1, device2) connections
        
    def add_device(self, device: NetworkDevice):
        """Add a device to the topology."""
        if device.name in self.devices:
            raise ValueError(f"Device '{device.name}' already exists")
        self.devices[device.name] = device
        
    def add_computer(self, name: str) -> Computer:
        """Add a computer to the topology."""
        computer = Computer(name)
        self.add_device(computer)
        return computer
        
    def add_router(self, name: str) -> Router:
        """Add a router to the topology."""
        router = Router(name)
        self.add_device(router)
        return router
        
    def add_switch(self, name: str) -> Switch:
        """Add a switch to the topology."""
        switch = Switch(name)
        self.add_device(switch)
        return switch
    
    def get_device(self, name: str) -> Optional[NetworkDevice]:
        """Get a device by name."""
        return self.devices.get(name)
    
    def connect_devices(self, device1_name: str, interface1: str, 
                       device2_name: str, interface2: str):
        """Connect two devices via their interfaces."""
        device1 = self.devices.get(device1_name)
        device2 = self.devices.get(device2_name)
        
        if not device1:
            raise ValueError(f"Device '{device1_name}' not found")
        if not device2:
            raise ValueError(f"Device '{device2_name}' not found")
        
        # Ensure interfaces exist
        if interface1 not in device1.interfaces:
            device1.add_interface(interface1)
        if interface2 not in device2.interfaces:
            device2.add_interface(interface2)
        
        # Connect interfaces
        device1.interfaces[interface1].connected_to = device2.interfaces[interface2]
        device2.interfaces[interface2].connected_to = device1.interfaces[interface1]
        
        # Track connection
        self.connections.append((f"{device1_name}:{interface1}", f"{device2_name}:{interface2}"))
        
    def find_device_by_ip(self, ip_address: str) -> Optional[NetworkDevice]:
        """Find a device that has the specified IP address."""
        for device in self.devices.values():
            for interface in device.interfaces.values():
                if interface.ip_address == ip_address:
                    return device
        return None
    
    def list_devices(self) -> List[str]:
        """List all devices in the topology."""
        return list(self.devices.keys())
    
    def get_device_info(self, device_name: str) -> Dict:
        """Get detailed information about a device."""
        device = self.devices.get(device_name)
        if not device:
            return {"error": f"Device '{device_name}' not found"}
        
        interfaces = {}
        for iface_name, iface in device.interfaces.items():
            interfaces[iface_name] = {
                "ip": iface.ip_address or "not configured",
                "mask": iface.subnet_mask or "N/A",
                "connected": iface.connected_to is not None
            }
        
        info = {
            "name": device.name,
            "type": device.device_type,
            "interfaces": interfaces
        }
        
        if isinstance(device, Computer) and device.default_gateway:
            info["gateway"] = device.default_gateway
            
        return info
    
    def show_topology(self) -> str:
        """Display the network topology as text."""
        output = ["Network Topology:", "=" * 50]
        
        for device_name, device in self.devices.items():
            output.append(f"\n{device}")
            for iface_name, iface in device.interfaces.items():
                output.append(f"  {iface}")
                if iface.connected_to:
                    connected_device = None
                    for dev in self.devices.values():
                        if iface.connected_to in dev.interfaces.values():
                            connected_device = dev
                            break
                    if connected_device:
                        output.append(f"    -> Connected to {connected_device.name}")
        
        output.append("\n" + "=" * 50)
        return "\n".join(output)

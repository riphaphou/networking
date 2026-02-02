"""Network device classes for the network simulation tool."""

import re
from typing import Optional, Dict, List


class NetworkInterface:
    """Represents a network interface on a device."""
    
    def __init__(self, name: str):
        self.name = name
        self.ip_address: Optional[str] = None
        self.subnet_mask: Optional[str] = None
        self.connected_to: Optional['NetworkInterface'] = None
        
    def configure_ip(self, ip_address: str, subnet_mask: str = "255.255.255.0"):
        """Configure IP address and subnet mask for this interface."""
        if not self._is_valid_ip(ip_address):
            raise ValueError(f"Invalid IP address: {ip_address}")
        if not self._is_valid_ip(subnet_mask):
            raise ValueError(f"Invalid subnet mask: {subnet_mask}")
        
        self.ip_address = ip_address
        self.subnet_mask = subnet_mask
        
    def _is_valid_ip(self, ip: str) -> bool:
        """Validate IP address format."""
        pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
        match = re.match(pattern, ip)
        if not match:
            return False
        return all(0 <= int(octet) <= 255 for octet in match.groups())
    
    def is_same_network(self, other_ip: str) -> bool:
        """Check if another IP is on the same network."""
        if not self.ip_address or not self.subnet_mask:
            return False
        
        def ip_to_int(ip: str) -> int:
            parts = [int(x) for x in ip.split('.')]
            return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]
        
        mask = ip_to_int(self.subnet_mask)
        this_network = ip_to_int(self.ip_address) & mask
        other_network = ip_to_int(other_ip) & mask
        
        return this_network == other_network
    
    def __str__(self):
        return f"{self.name}: {self.ip_address or 'not configured'}/{self.subnet_mask or 'N/A'}"


class NetworkDevice:
    """Base class for all network devices."""
    
    def __init__(self, name: str, device_type: str):
        self.name = name
        self.device_type = device_type
        self.interfaces: Dict[str, NetworkInterface] = {}
        self.routing_table: List[Dict] = []
        
    def add_interface(self, interface_name: str) -> NetworkInterface:
        """Add a network interface to this device."""
        interface = NetworkInterface(interface_name)
        self.interfaces[interface_name] = interface
        return interface
    
    def configure_interface(self, interface_name: str, ip_address: str, subnet_mask: str = "255.255.255.0"):
        """Configure an interface with IP address."""
        if interface_name not in self.interfaces:
            self.add_interface(interface_name)
        self.interfaces[interface_name].configure_ip(ip_address, subnet_mask)
        
    def get_interface(self, name: str) -> Optional[NetworkInterface]:
        """Get an interface by name."""
        return self.interfaces.get(name)
    
    def __str__(self):
        return f"{self.device_type} '{self.name}'"


class Computer(NetworkDevice):
    """Represents a computer/PC in the network."""
    
    def __init__(self, name: str):
        super().__init__(name, "Computer")
        self.default_gateway: Optional[str] = None
        # Add default interface
        self.add_interface("eth0")
        
    def set_default_gateway(self, gateway_ip: str):
        """Set the default gateway for this computer."""
        self.default_gateway = gateway_ip
        
    def ping(self, target_ip: str, network_topology) -> Dict:
        """Simulate a ping to a target IP address."""
        # Get the primary interface
        primary_interface = self.interfaces.get("eth0")
        
        if not primary_interface or not primary_interface.ip_address:
            return {
                "success": False,
                "message": f"Interface not configured on {self.name}",
                "hops": []
            }
        
        # Check if pinging self
        if target_ip == primary_interface.ip_address:
            return {
                "success": True,
                "message": f"Reply from {target_ip}: Self-ping successful",
                "hops": [self.name]
            }
        
        # Check if target is on the same network
        if primary_interface.is_same_network(target_ip):
            # Direct communication
            target_device = network_topology.find_device_by_ip(target_ip)
            if target_device:
                return {
                    "success": True,
                    "message": f"Reply from {target_ip}: bytes=32 time<1ms TTL=64",
                    "hops": [self.name, target_device.name]
                }
            else:
                return {
                    "success": False,
                    "message": f"Destination host {target_ip} unreachable",
                    "hops": [self.name]
                }
        else:
            # Need gateway
            if not self.default_gateway:
                return {
                    "success": False,
                    "message": f"No default gateway configured on {self.name}",
                    "hops": [self.name]
                }
            
            # Route through gateway
            gateway_device = network_topology.find_device_by_ip(self.default_gateway)
            if not gateway_device:
                return {
                    "success": False,
                    "message": f"Gateway {self.default_gateway} unreachable",
                    "hops": [self.name]
                }
            
            # For now, simple routing through gateway
            target_device = network_topology.find_device_by_ip(target_ip)
            if target_device:
                return {
                    "success": True,
                    "message": f"Reply from {target_ip}: bytes=32 time<1ms TTL=63",
                    "hops": [self.name, gateway_device.name, target_device.name]
                }
            else:
                return {
                    "success": False,
                    "message": f"Destination host {target_ip} unreachable",
                    "hops": [self.name, gateway_device.name]
                }


class Router(NetworkDevice):
    """Represents a router in the network."""
    
    def __init__(self, name: str):
        super().__init__(name, "Router")
        
    def add_route(self, network: str, mask: str, next_hop: str):
        """Add a static route to the routing table."""
        self.routing_table.append({
            "network": network,
            "mask": mask,
            "next_hop": next_hop
        })


class Switch(NetworkDevice):
    """Represents a switch in the network."""
    
    def __init__(self, name: str):
        super().__init__(name, "Switch")
        self.mac_table: Dict[str, str] = {}  # MAC to port mapping
        
    def learn_mac(self, mac_address: str, port: str):
        """Learn MAC address on a specific port."""
        self.mac_table[mac_address] = port

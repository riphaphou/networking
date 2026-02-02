#!/usr/bin/env python3
"""
Example 1: Simple two-computer network
Demonstrates basic IP configuration and ping testing
"""

from network_topology import NetworkTopology

def main():
    print("=" * 60)
    print("Example 1: Simple Two-Computer Network")
    print("=" * 60)
    
    # Create topology
    topology = NetworkTopology()
    
    # Add two computers
    print("\n1. Adding devices...")
    pc1 = topology.add_computer("PC1")
    pc2 = topology.add_computer("PC2")
    print(f"   ✓ Added {pc1}")
    print(f"   ✓ Added {pc2}")
    
    # Configure IP addresses
    print("\n2. Configuring IP addresses...")
    pc1.configure_interface("eth0", "192.168.1.10", "255.255.255.0")
    pc2.configure_interface("eth0", "192.168.1.20", "255.255.255.0")
    print(f"   ✓ PC1: 192.168.1.10/255.255.255.0")
    print(f"   ✓ PC2: 192.168.1.20/255.255.255.0")
    
    # Connect devices
    print("\n3. Connecting devices...")
    topology.connect_devices("PC1", "eth0", "PC2", "eth0")
    print(f"   ✓ Connected PC1:eth0 to PC2:eth0")
    
    # Show topology
    print("\n4. Network topology:")
    print(topology.show_topology())
    
    # Test ping
    print("\n5. Testing connectivity...")
    print("\n   Pinging from PC1 to PC2 (192.168.1.20):")
    result = pc1.ping("192.168.1.20", topology)
    if result["success"]:
        print(f"   ✓ {result['message']}")
        print(f"   Path: {' -> '.join(result['hops'])}")
    else:
        print(f"   ✗ {result['message']}")
    
    print("\n   Pinging from PC2 to PC1 (192.168.1.10):")
    result = pc2.ping("192.168.1.10", topology)
    if result["success"]:
        print(f"   ✓ {result['message']}")
        print(f"   Path: {' -> '.join(result['hops'])}")
    else:
        print(f"   ✗ {result['message']}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Example 2: Network with Router
Demonstrates routing between different subnets
"""

from network_topology import NetworkTopology

def main():
    print("=" * 60)
    print("Example 2: Network with Router (Two Subnets)")
    print("=" * 60)
    
    # Create topology
    topology = NetworkTopology()
    
    # Add devices
    print("\n1. Adding devices...")
    pc1 = topology.add_computer("PC1")
    pc2 = topology.add_computer("PC2")
    router = topology.add_router("R1")
    print(f"   ✓ Added {pc1}")
    print(f"   ✓ Added {pc2}")
    print(f"   ✓ Added {router}")
    
    # Configure IP addresses
    print("\n2. Configuring IP addresses...")
    
    # Network 1: 192.168.1.0/24
    pc1.configure_interface("eth0", "192.168.1.10", "255.255.255.0")
    router.add_interface("eth0")
    router.configure_interface("eth0", "192.168.1.1", "255.255.255.0")
    print(f"   ✓ Network 1 (192.168.1.0/24):")
    print(f"     - PC1: 192.168.1.10")
    print(f"     - R1:eth0: 192.168.1.1")
    
    # Network 2: 192.168.2.0/24
    pc2.configure_interface("eth0", "192.168.2.10", "255.255.255.0")
    router.add_interface("eth1")
    router.configure_interface("eth1", "192.168.2.1", "255.255.255.0")
    print(f"   ✓ Network 2 (192.168.2.0/24):")
    print(f"     - PC2: 192.168.2.10")
    print(f"     - R1:eth1: 192.168.2.1")
    
    # Set gateways
    print("\n3. Setting default gateways...")
    pc1.set_default_gateway("192.168.1.1")
    pc2.set_default_gateway("192.168.2.1")
    print(f"   ✓ PC1 gateway: 192.168.1.1")
    print(f"   ✓ PC2 gateway: 192.168.2.1")
    
    # Connect devices
    print("\n4. Connecting devices...")
    topology.connect_devices("PC1", "eth0", "R1", "eth0")
    topology.connect_devices("PC2", "eth0", "R1", "eth1")
    print(f"   ✓ Connected PC1:eth0 to R1:eth0")
    print(f"   ✓ Connected PC2:eth0 to R1:eth1")
    
    # Show topology
    print("\n5. Network topology:")
    print(topology.show_topology())
    
    # Test ping between different networks
    print("\n6. Testing inter-network connectivity...")
    print("\n   Pinging from PC1 (192.168.1.10) to PC2 (192.168.2.10):")
    result = pc1.ping("192.168.2.10", topology)
    if result["success"]:
        print(f"   ✓ {result['message']}")
        print(f"   Path: {' -> '.join(result['hops'])}")
    else:
        print(f"   ✗ {result['message']}")
    
    print("\n   Pinging from PC2 (192.168.2.10) to PC1 (192.168.1.10):")
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

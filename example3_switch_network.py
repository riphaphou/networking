#!/usr/bin/env python3
"""
Example 3: Network with Switch
Demonstrates a switched network with multiple computers
"""

from network_topology import NetworkTopology

def main():
    print("=" * 60)
    print("Example 3: Switched Network")
    print("=" * 60)
    
    # Create topology
    topology = NetworkTopology()
    
    # Add devices
    print("\n1. Adding devices...")
    pc1 = topology.add_computer("PC1")
    pc2 = topology.add_computer("PC2")
    pc3 = topology.add_computer("PC3")
    switch = topology.add_switch("SW1")
    print(f"   ✓ Added {pc1}")
    print(f"   ✓ Added {pc2}")
    print(f"   ✓ Added {pc3}")
    print(f"   ✓ Added {switch}")
    
    # Configure IP addresses (all on same network)
    print("\n2. Configuring IP addresses (192.168.1.0/24)...")
    pc1.configure_interface("eth0", "192.168.1.10", "255.255.255.0")
    pc2.configure_interface("eth0", "192.168.1.20", "255.255.255.0")
    pc3.configure_interface("eth0", "192.168.1.30", "255.255.255.0")
    print(f"   ✓ PC1: 192.168.1.10")
    print(f"   ✓ PC2: 192.168.1.20")
    print(f"   ✓ PC3: 192.168.1.30")
    
    # Connect all PCs to switch
    print("\n3. Connecting devices to switch...")
    topology.connect_devices("PC1", "eth0", "SW1", "port1")
    topology.connect_devices("PC2", "eth0", "SW1", "port2")
    topology.connect_devices("PC3", "eth0", "SW1", "port3")
    print(f"   ✓ Connected PC1:eth0 to SW1:port1")
    print(f"   ✓ Connected PC2:eth0 to SW1:port2")
    print(f"   ✓ Connected PC3:eth0 to SW1:port3")
    
    # Show topology
    print("\n4. Network topology:")
    print(topology.show_topology())
    
    # Test ping between all computers
    print("\n5. Testing connectivity...")
    
    tests = [
        (pc1, "PC1", "192.168.1.20", "PC2"),
        (pc1, "PC1", "192.168.1.30", "PC3"),
        (pc2, "PC2", "192.168.1.30", "PC3"),
    ]
    
    for source, source_name, target_ip, target_name in tests:
        print(f"\n   Pinging from {source_name} to {target_name} ({target_ip}):")
        result = source.ping(target_ip, topology)
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

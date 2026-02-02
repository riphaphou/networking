#!/usr/bin/env python3
"""
Unit tests for the network simulator
"""

import unittest
from network_device import Computer, Router, Switch, NetworkInterface
from network_topology import NetworkTopology


class TestNetworkInterface(unittest.TestCase):
    """Tests for NetworkInterface class."""
    
    def test_create_interface(self):
        """Test creating a network interface."""
        iface = NetworkInterface("eth0")
        self.assertEqual(iface.name, "eth0")
        self.assertIsNone(iface.ip_address)
        self.assertIsNone(iface.subnet_mask)
        
    def test_configure_ip(self):
        """Test configuring IP address."""
        iface = NetworkInterface("eth0")
        iface.configure_ip("192.168.1.10", "255.255.255.0")
        self.assertEqual(iface.ip_address, "192.168.1.10")
        self.assertEqual(iface.subnet_mask, "255.255.255.0")
        
    def test_invalid_ip(self):
        """Test invalid IP address."""
        iface = NetworkInterface("eth0")
        with self.assertRaises(ValueError):
            iface.configure_ip("999.999.999.999", "255.255.255.0")
        with self.assertRaises(ValueError):
            iface.configure_ip("192.168.1", "255.255.255.0")
            
    def test_same_network(self):
        """Test same network detection."""
        iface = NetworkInterface("eth0")
        iface.configure_ip("192.168.1.10", "255.255.255.0")
        
        self.assertTrue(iface.is_same_network("192.168.1.20"))
        self.assertTrue(iface.is_same_network("192.168.1.1"))
        self.assertFalse(iface.is_same_network("192.168.2.10"))
        self.assertFalse(iface.is_same_network("10.0.0.1"))


class TestComputer(unittest.TestCase):
    """Tests for Computer class."""
    
    def test_create_computer(self):
        """Test creating a computer."""
        pc = Computer("PC1")
        self.assertEqual(pc.name, "PC1")
        self.assertEqual(pc.device_type, "Computer")
        self.assertIn("eth0", pc.interfaces)
        
    def test_configure_interface(self):
        """Test configuring interface on computer."""
        pc = Computer("PC1")
        pc.configure_interface("eth0", "192.168.1.10", "255.255.255.0")
        
        iface = pc.get_interface("eth0")
        self.assertEqual(iface.ip_address, "192.168.1.10")
        self.assertEqual(iface.subnet_mask, "255.255.255.0")
        
    def test_set_gateway(self):
        """Test setting default gateway."""
        pc = Computer("PC1")
        pc.set_default_gateway("192.168.1.1")
        self.assertEqual(pc.default_gateway, "192.168.1.1")


class TestRouter(unittest.TestCase):
    """Tests for Router class."""
    
    def test_create_router(self):
        """Test creating a router."""
        router = Router("R1")
        self.assertEqual(router.name, "R1")
        self.assertEqual(router.device_type, "Router")
        
    def test_add_interface(self):
        """Test adding interface to router."""
        router = Router("R1")
        router.add_interface("eth0")
        router.add_interface("eth1")
        
        self.assertIn("eth0", router.interfaces)
        self.assertIn("eth1", router.interfaces)
        
    def test_add_route(self):
        """Test adding static route."""
        router = Router("R1")
        router.add_route("192.168.2.0", "255.255.255.0", "192.168.1.1")
        
        self.assertEqual(len(router.routing_table), 1)
        self.assertEqual(router.routing_table[0]["network"], "192.168.2.0")


class TestSwitch(unittest.TestCase):
    """Tests for Switch class."""
    
    def test_create_switch(self):
        """Test creating a switch."""
        switch = Switch("SW1")
        self.assertEqual(switch.name, "SW1")
        self.assertEqual(switch.device_type, "Switch")
        
    def test_learn_mac(self):
        """Test MAC address learning."""
        switch = Switch("SW1")
        switch.learn_mac("00:11:22:33:44:55", "port1")
        
        self.assertIn("00:11:22:33:44:55", switch.mac_table)
        self.assertEqual(switch.mac_table["00:11:22:33:44:55"], "port1")


class TestNetworkTopology(unittest.TestCase):
    """Tests for NetworkTopology class."""
    
    def test_add_device(self):
        """Test adding devices to topology."""
        topology = NetworkTopology()
        
        pc = Computer("PC1")
        topology.add_device(pc)
        
        self.assertIn("PC1", topology.devices)
        self.assertEqual(topology.devices["PC1"], pc)
        
    def test_add_duplicate_device(self):
        """Test adding duplicate device raises error."""
        topology = NetworkTopology()
        
        pc1 = Computer("PC1")
        topology.add_device(pc1)
        
        pc2 = Computer("PC1")
        with self.assertRaises(ValueError):
            topology.add_device(pc2)
            
    def test_add_computer(self):
        """Test add_computer helper method."""
        topology = NetworkTopology()
        pc = topology.add_computer("PC1")
        
        self.assertIsInstance(pc, Computer)
        self.assertIn("PC1", topology.devices)
        
    def test_connect_devices(self):
        """Test connecting two devices."""
        topology = NetworkTopology()
        
        pc1 = topology.add_computer("PC1")
        pc2 = topology.add_computer("PC2")
        
        topology.connect_devices("PC1", "eth0", "PC2", "eth0")
        
        iface1 = pc1.get_interface("eth0")
        iface2 = pc2.get_interface("eth0")
        
        self.assertEqual(iface1.connected_to, iface2)
        self.assertEqual(iface2.connected_to, iface1)
        
    def test_find_device_by_ip(self):
        """Test finding device by IP address."""
        topology = NetworkTopology()
        
        pc = topology.add_computer("PC1")
        pc.configure_interface("eth0", "192.168.1.10", "255.255.255.0")
        
        found = topology.find_device_by_ip("192.168.1.10")
        self.assertEqual(found, pc)
        
        not_found = topology.find_device_by_ip("192.168.1.20")
        self.assertIsNone(not_found)


class TestPing(unittest.TestCase):
    """Tests for ping functionality."""
    
    def test_ping_same_network(self):
        """Test ping on same network."""
        topology = NetworkTopology()
        
        pc1 = topology.add_computer("PC1")
        pc2 = topology.add_computer("PC2")
        
        pc1.configure_interface("eth0", "192.168.1.10", "255.255.255.0")
        pc2.configure_interface("eth0", "192.168.1.20", "255.255.255.0")
        
        topology.connect_devices("PC1", "eth0", "PC2", "eth0")
        
        result = pc1.ping("192.168.1.20", topology)
        self.assertTrue(result["success"])
        self.assertIn("PC1", result["hops"])
        self.assertIn("PC2", result["hops"])
        
    def test_ping_self(self):
        """Test pinging self."""
        topology = NetworkTopology()
        
        pc = topology.add_computer("PC1")
        pc.configure_interface("eth0", "192.168.1.10", "255.255.255.0")
        
        result = pc.ping("192.168.1.10", topology)
        self.assertTrue(result["success"])
        
    def test_ping_no_ip_configured(self):
        """Test ping when IP not configured."""
        topology = NetworkTopology()
        
        pc = topology.add_computer("PC1")
        
        result = pc.ping("192.168.1.20", topology)
        self.assertFalse(result["success"])
        
    def test_ping_unreachable(self):
        """Test ping to unreachable host."""
        topology = NetworkTopology()
        
        pc = topology.add_computer("PC1")
        pc.configure_interface("eth0", "192.168.1.10", "255.255.255.0")
        
        result = pc.ping("192.168.1.20", topology)
        self.assertFalse(result["success"])
        
    def test_ping_through_gateway(self):
        """Test ping through gateway to different network."""
        topology = NetworkTopology()
        
        pc1 = topology.add_computer("PC1")
        pc2 = topology.add_computer("PC2")
        router = topology.add_router("R1")
        
        # Configure Network 1
        pc1.configure_interface("eth0", "192.168.1.10", "255.255.255.0")
        router.configure_interface("eth0", "192.168.1.1", "255.255.255.0")
        
        # Configure Network 2
        pc2.configure_interface("eth0", "192.168.2.10", "255.255.255.0")
        router.configure_interface("eth1", "192.168.2.1", "255.255.255.0")
        
        # Set gateways
        pc1.set_default_gateway("192.168.1.1")
        pc2.set_default_gateway("192.168.2.1")
        
        # Connect devices
        topology.connect_devices("PC1", "eth0", "R1", "eth0")
        topology.connect_devices("PC2", "eth0", "R1", "eth1")
        
        # Test ping through router
        result = pc1.ping("192.168.2.10", topology)
        self.assertTrue(result["success"])
        self.assertIn("PC1", result["hops"])
        self.assertIn("R1", result["hops"])
        self.assertIn("PC2", result["hops"])


def run_tests():
    """Run all tests."""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()

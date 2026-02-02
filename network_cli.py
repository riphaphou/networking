"""Command-line interface for the network simulation tool."""

import cmd
from network_topology import NetworkTopology
from network_device import Computer


class NetworkSimulatorCLI(cmd.Cmd):
    """Interactive CLI for network simulation."""
    
    intro = """
╔══════════════════════════════════════════════════════════╗
║   Network Simulator - Similar to Cisco Packet Tracer    ║
╚══════════════════════════════════════════════════════════╝

Type 'help' or '?' to list available commands.
Type 'exit' or 'quit' to exit the simulator.
    """
    prompt = "NetSim> "
    
    def __init__(self):
        super().__init__()
        self.topology = NetworkTopology()
        
    def do_add_computer(self, arg):
        """Add a computer to the network: add_computer <name>"""
        if not arg:
            print("Usage: add_computer <name>")
            return
        try:
            computer = self.topology.add_computer(arg)
            print(f"✓ Computer '{arg}' added successfully")
        except ValueError as e:
            print(f"✗ Error: {e}")
            
    def do_add_router(self, arg):
        """Add a router to the network: add_router <name>"""
        if not arg:
            print("Usage: add_router <name>")
            return
        try:
            router = self.topology.add_router(arg)
            print(f"✓ Router '{arg}' added successfully")
        except ValueError as e:
            print(f"✗ Error: {e}")
            
    def do_add_switch(self, arg):
        """Add a switch to the network: add_switch <name>"""
        if not arg:
            print("Usage: add_switch <name>")
            return
        try:
            switch = self.topology.add_switch(arg)
            print(f"✓ Switch '{arg}' added successfully")
        except ValueError as e:
            print(f"✗ Error: {e}")
            
    def do_configure_ip(self, arg):
        """Configure IP on a device: configure_ip <device> <interface> <ip> [subnet_mask]"""
        args = arg.split()
        if len(args) < 3:
            print("Usage: configure_ip <device> <interface> <ip> [subnet_mask]")
            return
        
        device_name = args[0]
        interface = args[1]
        ip = args[2]
        mask = args[3] if len(args) > 3 else "255.255.255.0"
        
        device = self.topology.get_device(device_name)
        if not device:
            print(f"✗ Error: Device '{device_name}' not found")
            return
        
        try:
            device.configure_interface(interface, ip, mask)
            print(f"✓ Configured {device_name}:{interface} with IP {ip}/{mask}")
        except ValueError as e:
            print(f"✗ Error: {e}")
            
    def do_set_gateway(self, arg):
        """Set default gateway for a computer: set_gateway <computer> <gateway_ip>"""
        args = arg.split()
        if len(args) != 2:
            print("Usage: set_gateway <computer> <gateway_ip>")
            return
        
        device_name, gateway = args
        device = self.topology.get_device(device_name)
        
        if not device:
            print(f"✗ Error: Device '{device_name}' not found")
            return
        
        if not isinstance(device, Computer):
            print(f"✗ Error: '{device_name}' is not a computer")
            return
        
        device.set_default_gateway(gateway)
        print(f"✓ Default gateway set to {gateway} for {device_name}")
        
    def do_connect(self, arg):
        """Connect two devices: connect <device1> <interface1> <device2> <interface2>"""
        args = arg.split()
        if len(args) != 4:
            print("Usage: connect <device1> <interface1> <device2> <interface2>")
            return
        
        try:
            self.topology.connect_devices(args[0], args[1], args[2], args[3])
            print(f"✓ Connected {args[0]}:{args[1]} to {args[2]}:{args[3]}")
        except ValueError as e:
            print(f"✗ Error: {e}")
            
    def do_ping(self, arg):
        """Ping from a computer to a target IP: ping <computer> <target_ip>"""
        args = arg.split()
        if len(args) != 2:
            print("Usage: ping <computer> <target_ip>")
            return
        
        computer_name, target_ip = args
        device = self.topology.get_device(computer_name)
        
        if not device:
            print(f"✗ Error: Device '{computer_name}' not found")
            return
        
        if not isinstance(device, Computer):
            print(f"✗ Error: '{computer_name}' is not a computer")
            return
        
        print(f"\nPinging {target_ip} from {computer_name}...")
        result = device.ping(target_ip, self.topology)
        
        if result["success"]:
            print(f"✓ {result['message']}")
            print(f"  Path: {' -> '.join(result['hops'])}")
        else:
            print(f"✗ {result['message']}")
            if result['hops']:
                print(f"  Path traced: {' -> '.join(result['hops'])}")
                
    def do_show_topology(self, arg):
        """Display the current network topology"""
        print(self.topology.show_topology())
        
    def do_show_device(self, arg):
        """Show details of a specific device: show_device <device_name>"""
        if not arg:
            print("Usage: show_device <device_name>")
            return
        
        info = self.topology.get_device_info(arg)
        if "error" in info:
            print(f"✗ {info['error']}")
            return
        
        print(f"\nDevice Information: {info['name']}")
        print(f"Type: {info['type']}")
        print("Interfaces:")
        for iface, data in info['interfaces'].items():
            print(f"  {iface}:")
            print(f"    IP: {data['ip']}")
            print(f"    Mask: {data['mask']}")
            print(f"    Connected: {'Yes' if data['connected'] else 'No'}")
        
        if 'gateway' in info:
            print(f"Default Gateway: {info['gateway']}")
            
    def do_list(self, arg):
        """List all devices in the network"""
        devices = self.topology.list_devices()
        if not devices:
            print("No devices in the network")
            return
        
        print("\nDevices in network:")
        for device_name in devices:
            device = self.topology.get_device(device_name)
            print(f"  - {device}")
            
    def do_quit(self, arg):
        """Exit the network simulator"""
        print("Exiting network simulator...")
        return True
        
    def do_exit(self, arg):
        """Exit the network simulator"""
        return self.do_quit(arg)
        
    def do_clear(self, arg):
        """Clear the screen"""
        print("\033[2J\033[H")


def main():
    """Main entry point for the CLI."""
    NetworkSimulatorCLI().cmdloop()


if __name__ == "__main__":
    main()

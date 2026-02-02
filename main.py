#!/usr/bin/env python3
"""
Network Simulator - Similar to Cisco Packet Tracer
Main entry point for the application.
"""

import sys
import argparse


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Network Simulator - Similar to Cisco Packet Tracer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              # Start GUI mode (default)
  python main.py --gui        # Start GUI mode
  python main.py --cli        # Start CLI mode
  
Features:
  - Create network topologies with computers, routers, and switches
  - Configure IP addresses and subnet masks
  - Set up gateways for routing
  - Test connectivity with ping
  - Visual network diagram (GUI mode)
        """
    )
    
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Start in CLI mode instead of GUI mode'
    )
    
    parser.add_argument(
        '--gui',
        action='store_true',
        help='Start in GUI mode (default)'
    )
    
    args = parser.parse_args()
    
    # Determine which mode to use
    use_cli = args.cli and not args.gui
    
    if use_cli:
        print("Starting Network Simulator in CLI mode...")
        from network_cli import main as cli_main
        cli_main()
    else:
        print("Starting Network Simulator in GUI mode...")
        try:
            from network_gui import main as gui_main
            gui_main()
        except ImportError as e:
            print(f"Error: Could not start GUI mode: {e}")
            print("Tkinter might not be installed. Try running in CLI mode with --cli")
            sys.exit(1)


if __name__ == "__main__":
    main()

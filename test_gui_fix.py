#!/usr/bin/env python3
"""
Test script to verify GUI can be initialized without errors.
This tests the fix for the AttributeError with canvas.master.
"""

import sys
import os

# Test if tkinter is available
try:
    import tkinter as tk
    from tkinter import ttk
    print("✓ tkinter is available")
except ImportError as e:
    print(f"✗ tkinter is not available: {e}")
    print("Skipping GUI test (expected in headless environment)")
    sys.exit(0)

# Import our modules
from network_gui import NetworkSimulatorGUI, DeviceIcon
from network_topology import NetworkTopology
from network_device import Computer

print("\n" + "=" * 60)
print("GUI Initialization Test")
print("=" * 60)

try:
    # Create root window
    root = tk.Tk()
    root.withdraw()  # Don't show the window
    
    print("\n[1] Creating NetworkSimulatorGUI instance...")
    app = NetworkSimulatorGUI(root)
    print("✓ NetworkSimulatorGUI created successfully")
    
    print("\n[2] Checking canvas.gui_app attribute...")
    assert hasattr(app.canvas, 'gui_app'), "canvas should have gui_app attribute"
    assert app.canvas.gui_app == app, "canvas.gui_app should reference the app"
    print("✓ canvas.gui_app is correctly set")
    
    print("\n[3] Testing DeviceIcon creation...")
    pc = Computer("TestPC")
    icon = DeviceIcon(app.canvas, pc, 100, 100)
    print("✓ DeviceIcon created successfully")
    
    print("\n[4] Testing canvas.master (tkinter property)...")
    # This should still work and return the tkinter parent
    canvas_parent = app.canvas.master
    print(f"✓ canvas.master returns: {type(canvas_parent).__name__}")
    
    print("\n[5] Simulating device drag (to test redraw_connections call)...")
    # Create a mock event
    class MockEvent:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    # Initialize drag data
    icon._drag_data = {"x": 100, "y": 100}
    
    # Try to call on_drag - this would previously fail with AttributeError
    try:
        event = MockEvent(110, 110)
        icon.on_drag(event)
        print("✓ on_drag() executed without AttributeError")
    except AttributeError as e:
        if "'NetworkSimulatorGUI' object has no attribute 'master'" in str(e):
            print(f"✗ FAILED: Still getting the original error: {e}")
            sys.exit(1)
        else:
            raise
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nThe GUI fix is working correctly.")
    print("canvas.master is preserved for tkinter")
    print("canvas.gui_app is used for our custom reference")
    
    root.destroy()
    
except Exception as e:
    print(f"\n✗ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

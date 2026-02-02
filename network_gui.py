"""Graphical user interface for the network simulation tool."""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from network_topology import NetworkTopology
from network_device import Computer, Router, Switch
import math


class DeviceIcon:
    """Represents a device icon on the canvas."""
    
    def __init__(self, canvas, device, x, y):
        self.canvas = canvas
        self.device = device
        self.x = x
        self.y = y
        self.size = 50
        
        # Draw device based on type
        self.draw()
        
        # Bind events
        self.canvas.tag_bind(self.tag, '<Button-1>', self.on_click)
        self.canvas.tag_bind(self.tag, '<B1-Motion>', self.on_drag)
        
    def draw(self):
        """Draw the device icon."""
        self.tag = f"device_{self.device.name}"
        
        # Choose color based on device type
        if isinstance(self.device, Computer):
            color = "#4CAF50"
            symbol = "💻"
        elif isinstance(self.device, Router):
            color = "#2196F3"
            symbol = "🔀"
        elif isinstance(self.device, Switch):
            color = "#FF9800"
            symbol = "⚡"
        else:
            color = "#9E9E9E"
            symbol = "?"
        
        # Draw rectangle
        self.canvas.create_rectangle(
            self.x - self.size//2, self.y - self.size//2,
            self.x + self.size//2, self.y + self.size//2,
            fill=color, outline="black", width=2, tags=self.tag
        )
        
        # Draw symbol
        self.canvas.create_text(
            self.x, self.y - 10,
            text=symbol, font=("Arial", 20), tags=self.tag
        )
        
        # Draw name
        self.canvas.create_text(
            self.x, self.y + 15,
            text=self.device.name, font=("Arial", 9, "bold"), tags=self.tag
        )
        
    def on_click(self, event):
        """Handle click event."""
        self._drag_data = {"x": event.x, "y": event.y}
        
    def on_drag(self, event):
        """Handle drag event."""
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        
        self.canvas.move(self.tag, dx, dy)
        self.x += dx
        self.y += dy
        
        self._drag_data = {"x": event.x, "y": event.y}
        
        # Redraw connections
        self.canvas.master.redraw_connections()


class NetworkSimulatorGUI:
    """Main GUI application for network simulation."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Network Simulator - Like Cisco Packet Tracer")
        self.root.geometry("1200x800")
        
        self.topology = NetworkTopology()
        self.device_icons = {}
        self.connection_lines = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create toolbar
        toolbar = ttk.Frame(main_frame, relief=tk.RAISED, borderwidth=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Add device buttons
        ttk.Button(toolbar, text="➕ Computer", command=self.add_computer).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(toolbar, text="➕ Router", command=self.add_router).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(toolbar, text="➕ Switch", command=self.add_switch).pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(toolbar, text="🔧 Configure IP", command=self.configure_ip).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(toolbar, text="🌐 Set Gateway", command=self.set_gateway).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(toolbar, text="🔗 Connect", command=self.connect_devices).pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(toolbar, text="📡 Ping", command=self.ping).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(toolbar, text="ℹ️ Info", command=self.show_device_info).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Create canvas for drawing network
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", width=900, height=700)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Store reference for redrawing connections
        self.canvas.master = self
        
        # Create info panel
        info_frame = ttk.Frame(main_frame, width=300)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        
        ttk.Label(info_frame, text="Network Information", font=("Arial", 12, "bold")).pack(pady=5)
        
        self.info_text = tk.Text(info_frame, width=35, height=40, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(info_frame, command=self.info_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text.config(yscrollcommand=scrollbar.set)
        
        self.update_info_panel()
        
    def add_computer(self):
        """Add a computer to the network."""
        name = simpledialog.askstring("Add Computer", "Enter computer name:")
        if name:
            try:
                computer = self.topology.add_computer(name)
                x = 100 + len(self.device_icons) * 100 % 700
                y = 100 + (len(self.device_icons) // 7) * 100
                icon = DeviceIcon(self.canvas, computer, x, y)
                self.device_icons[name] = icon
                self.update_info_panel()
                messagebox.showinfo("Success", f"Computer '{name}' added successfully")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                
    def add_router(self):
        """Add a router to the network."""
        name = simpledialog.askstring("Add Router", "Enter router name:")
        if name:
            try:
                router = self.topology.add_router(name)
                x = 100 + len(self.device_icons) * 100 % 700
                y = 100 + (len(self.device_icons) // 7) * 100
                icon = DeviceIcon(self.canvas, router, x, y)
                self.device_icons[name] = icon
                self.update_info_panel()
                messagebox.showinfo("Success", f"Router '{name}' added successfully")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                
    def add_switch(self):
        """Add a switch to the network."""
        name = simpledialog.askstring("Add Switch", "Enter switch name:")
        if name:
            try:
                switch = self.topology.add_switch(name)
                x = 100 + len(self.device_icons) * 100 % 700
                y = 100 + (len(self.device_icons) // 7) * 100
                icon = DeviceIcon(self.canvas, switch, x, y)
                self.device_icons[name] = icon
                self.update_info_panel()
                messagebox.showinfo("Success", f"Switch '{name}' added successfully")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                
    def configure_ip(self):
        """Configure IP address on a device."""
        devices = self.topology.list_devices()
        if not devices:
            messagebox.showwarning("Warning", "No devices to configure")
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Configure IP Address")
        dialog.geometry("400x250")
        
        ttk.Label(dialog, text="Device:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        device_var = tk.StringVar()
        device_combo = ttk.Combobox(dialog, textvariable=device_var, values=devices, width=30)
        device_combo.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Interface:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        interface_var = tk.StringVar(value="eth0")
        ttk.Entry(dialog, textvariable=interface_var, width=32).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="IP Address:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        ip_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=ip_var, width=32).grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Subnet Mask:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        mask_var = tk.StringVar(value="255.255.255.0")
        ttk.Entry(dialog, textvariable=mask_var, width=32).grid(row=3, column=1, padx=10, pady=5)
        
        def apply():
            device = self.topology.get_device(device_var.get())
            if device:
                try:
                    device.configure_interface(interface_var.get(), ip_var.get(), mask_var.get())
                    self.update_info_panel()
                    messagebox.showinfo("Success", "IP configured successfully")
                    dialog.destroy()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showerror("Error", "Device not found")
        
        ttk.Button(dialog, text="Apply", command=apply).grid(row=4, column=0, columnspan=2, pady=20)
        
    def set_gateway(self):
        """Set default gateway for a computer."""
        computers = [name for name, dev in self.topology.devices.items() if isinstance(dev, Computer)]
        if not computers:
            messagebox.showwarning("Warning", "No computers to configure")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Set Default Gateway")
        dialog.geometry("400x150")
        
        ttk.Label(dialog, text="Computer:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        computer_var = tk.StringVar()
        ttk.Combobox(dialog, textvariable=computer_var, values=computers, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Gateway IP:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        gateway_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=gateway_var, width=32).grid(row=1, column=1, padx=10, pady=5)
        
        def apply():
            device = self.topology.get_device(computer_var.get())
            if device and isinstance(device, Computer):
                device.set_default_gateway(gateway_var.get())
                self.update_info_panel()
                messagebox.showinfo("Success", "Gateway set successfully")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Computer not found")
        
        ttk.Button(dialog, text="Apply", command=apply).grid(row=2, column=0, columnspan=2, pady=20)
        
    def connect_devices(self):
        """Connect two devices."""
        devices = self.topology.list_devices()
        if len(devices) < 2:
            messagebox.showwarning("Warning", "Need at least 2 devices to connect")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Connect Devices")
        dialog.geometry("400x220")
        
        ttk.Label(dialog, text="Device 1:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        dev1_var = tk.StringVar()
        ttk.Combobox(dialog, textvariable=dev1_var, values=devices, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Interface 1:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        int1_var = tk.StringVar(value="eth0")
        ttk.Entry(dialog, textvariable=int1_var, width=32).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Device 2:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        dev2_var = tk.StringVar()
        ttk.Combobox(dialog, textvariable=dev2_var, values=devices, width=30).grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Interface 2:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        int2_var = tk.StringVar(value="eth0")
        ttk.Entry(dialog, textvariable=int2_var, width=32).grid(row=3, column=1, padx=10, pady=5)
        
        def apply():
            try:
                self.topology.connect_devices(dev1_var.get(), int1_var.get(), dev2_var.get(), int2_var.get())
                self.redraw_connections()
                self.update_info_panel()
                messagebox.showinfo("Success", "Devices connected successfully")
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Connect", command=apply).grid(row=4, column=0, columnspan=2, pady=20)
        
    def ping(self):
        """Perform a ping test."""
        computers = [name for name, dev in self.topology.devices.items() if isinstance(dev, Computer)]
        if not computers:
            messagebox.showwarning("Warning", "No computers to ping from")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Ping Test")
        dialog.geometry("400x150")
        
        ttk.Label(dialog, text="Source Computer:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        source_var = tk.StringVar()
        ttk.Combobox(dialog, textvariable=source_var, values=computers, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Target IP:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        target_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=target_var, width=32).grid(row=1, column=1, padx=10, pady=5)
        
        def execute():
            device = self.topology.get_device(source_var.get())
            if device and isinstance(device, Computer):
                result = device.ping(target_var.get(), self.topology)
                
                result_text = f"Ping Result:\n\n"
                result_text += f"Source: {source_var.get()}\n"
                result_text += f"Target: {target_var.get()}\n\n"
                result_text += f"Status: {'SUCCESS ✓' if result['success'] else 'FAILED ✗'}\n"
                result_text += f"Message: {result['message']}\n"
                if result['hops']:
                    result_text += f"\nPath: {' -> '.join(result['hops'])}"
                
                messagebox.showinfo("Ping Result", result_text)
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Computer not found")
        
        ttk.Button(dialog, text="Ping", command=execute).grid(row=2, column=0, columnspan=2, pady=20)
        
    def show_device_info(self):
        """Show detailed device information."""
        devices = self.topology.list_devices()
        if not devices:
            messagebox.showwarning("Warning", "No devices in the network")
            return
        
        device_name = simpledialog.askstring("Device Info", f"Enter device name:\n{', '.join(devices)}")
        if device_name:
            info = self.topology.get_device_info(device_name)
            if "error" in info:
                messagebox.showerror("Error", info["error"])
            else:
                info_text = f"Device: {info['name']}\n"
                info_text += f"Type: {info['type']}\n\n"
                info_text += "Interfaces:\n"
                for iface, data in info['interfaces'].items():
                    info_text += f"  {iface}:\n"
                    info_text += f"    IP: {data['ip']}\n"
                    info_text += f"    Mask: {data['mask']}\n"
                    info_text += f"    Connected: {'Yes' if data['connected'] else 'No'}\n"
                if 'gateway' in info:
                    info_text += f"\nDefault Gateway: {info['gateway']}"
                
                messagebox.showinfo("Device Information", info_text)
                
    def redraw_connections(self):
        """Redraw all connections between devices."""
        # Remove old connection lines
        for line in self.connection_lines:
            self.canvas.delete(line)
        self.connection_lines = []
        
        # Draw new connections
        for connection in self.topology.connections:
            dev1_info, dev2_info = connection
            dev1_name = dev1_info.split(':')[0]
            dev2_name = dev2_info.split(':')[0]
            
            if dev1_name in self.device_icons and dev2_name in self.device_icons:
                icon1 = self.device_icons[dev1_name]
                icon2 = self.device_icons[dev2_name]
                
                line = self.canvas.create_line(
                    icon1.x, icon1.y, icon2.x, icon2.y,
                    fill="blue", width=2, dash=(5, 5)
                )
                self.canvas.tag_lower(line)
                self.connection_lines.append(line)
                
    def update_info_panel(self):
        """Update the information panel."""
        self.info_text.delete(1.0, tk.END)
        
        devices = self.topology.list_devices()
        self.info_text.insert(tk.END, f"Total Devices: {len(devices)}\n\n")
        
        for device_name in devices:
            info = self.topology.get_device_info(device_name)
            self.info_text.insert(tk.END, f"━━━ {info['name']} ({info['type']}) ━━━\n")
            
            for iface, data in info['interfaces'].items():
                self.info_text.insert(tk.END, f"  {iface}: {data['ip']}\n")
            
            if 'gateway' in info:
                self.info_text.insert(tk.END, f"  Gateway: {info['gateway']}\n")
            
            self.info_text.insert(tk.END, "\n")


def main():
    """Main entry point for the GUI."""
    root = tk.Tk()
    app = NetworkSimulatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# Bug Fix: GUI AttributeError

## Issue
When running the GUI mode (`python main.py`), the application would crash with:
```
AttributeError: 'NetworkSimulatorGUI' object has no attribute 'master'
```

## Root Cause
The code was overwriting the `canvas.master` property (line 131 in `network_gui.py`):
```python
self.canvas.master = self
```

The `master` property is a tkinter internal property that refers to the parent widget. Overwriting it with our `NetworkSimulatorGUI` object broke tkinter's widget hierarchy traversal, causing the AttributeError when tkinter tried to access the widget tree.

## Solution
Changed from using `canvas.master` to a custom attribute `canvas.gui_app`:
- Line 131: `self.canvas.gui_app = self` (instead of `self.canvas.master = self`)
- Line 80 in `DeviceIcon.on_drag()`: `self.canvas.gui_app.redraw_connections()` (instead of `self.canvas.master.redraw_connections()`)

This preserves tkinter's internal `master` property while still allowing `DeviceIcon` to access the main GUI application for redrawing connections.

## Testing
- All 22 existing unit tests still pass
- CLI mode works correctly
- GUI initialization works without AttributeError (verified in code review)

## Files Changed
- `network_gui.py`: Lines 80 and 131

# 🖱️ MAkCU Button Debugger

**Version 1.1 - 5/25/25**

A Python-based utility to connect to a CH343 USB serial device (MAkCU), switch to 4M baud for high-speed communication, and display the state of mouse-like buttons in real-time using a terminal UI.



## 🚀 Features

- Automatically detects the **CH343** serial device (`USB-Enhanced-SERIAL CH343`)
- Falls back to a custom COM port if auto-detection fails
- Establishes serial communication at `115200` baud, then switches to `4M` baud for optimal speed
- Sends initialization command: `km.buttons(1)`
- Starts a background listener thread to:
  - Read button press data in real-time
  - Display current connection and button states
  - Maintain a live log window within the terminal
- Color-coded terminal UI for easy visualization of button states:
  - 🟩 Green: Pressed
  - 🟥 Red: Unpressed


## 🧰 Requirements

- Python 3.7+
- `pyserial`

Install with:

```
pip install pyserial
```


## 🎮 Button Mapping

The script supports detection of the following buttons:

| Bit | Button               |
|-----|----------------------|
| 0   | Left Mouse           |
| 1   | Right Mouse          |
| 2   | Middle Mouse         |
| 3   | Side Button 4        |
| 4   | Side Button 5        |



## ⚙️ How It Works

1. **Device Detection:**
   - Searches for `"USB-Enhanced-SERIAL CH343"` via `serial.tools.list_ports`.
   - If not found, falls back to `COM1` or user-defined port.

2. **Connection and Baud Rate Switch:**
   - Connects at `115200` baud.
   - Sends special command to request switching to `4M` baud.
   - Reopens the port at `4000000` baud.

3. **Listening and Output:**
   - Reads button byte data.
   - Updates the console UI live with button press status and logs.



## 🛠️ Configuration

You can modify the fallback COM port in the script:

```
fallback_com_port = "COM1"  # <- Change to your port
```



## 🧪 Running the Script

Run the script directly in your terminal:

```
python v1.1-example.py
```

To stop the script, press `Ctrl+C`.



## 🧯 Graceful Shutdown

On `KeyboardInterrupt`, the script:
- Closes the serial port
- Joins the listener thread
- Logs shutdown and exits cleanly



## 📋 Example Output

```
Port: COM5 | Baud Rate: 4000000 | Connected: True

---== Log ==---
[12:34:56] Searching for CH343 Device...
[12:34:56] Device found: COM1
[12:34:56] Trying to open COM1 at 115200 baud.
[12:34:56] Connected to COM1 at 115200.
[12:34:56] Sending baud rate switch command to 4M
[12:34:56] Trying to open COM1 at 4000000 baud.
[12:34:57] Switched to 4M baud successfully.
[12:34:57] Sending init command: km.buttons(1)
[12:34:57] Started listening thread for button states.
---== Button States ==---
Left Mouse Button: 🟥 Unpressed  
Right Mouse Button: 🟩 Pressed  
Middle Mouse Button: 🟥 Unpressed  
Side Mouse 4 Button: 🟥 Unpressed  
Side Mouse 5 Button: 🟥 Unpressed  
---== Button States ==---
```



## 📎 Notes

- Windows users: If the port is in use or inaccessible, a `PermissionError` will be logged.
- Set fallback COM port in `v1.1-example.py`:
```
fallback_com_port = "COM1"  # Change if needed
```

## Troubleshooting
**Device not found?**
1. Install [CH343 driver](https://github.com/SleepyTotem/Makcu-Examples/releases/tag/Driver)
2. Check COM port in Device Manager
3. Update `fallback_com_port`


## License
This project is licensed under the terms of the [GNU General Public License v3.0 or later](https://www.gnu.org/licenses/gpl-3.0.html).

**You may:**
- Use freely  
- Modify and redistribute  
- Use for personal and commercial projects  

**You may not:**
- Sell this software directly without compliance with the GPL  

**Attribution required**

# Version 1.0 - 5/11/25

import serial
import time
import threading
import os

from serial.tools import list_ports

# Command to change the baud rate to 4M
baud_change_command = bytearray([0xDE, 0xAD, 0x05, 0x00, 0xA5, 0x00, 0x09, 0x3D, 0x00])

# Global variables
makcu = None
makcu_lock = threading.Lock()
is_connected = False
current_com_port = None
current_baud_rate = None
listener_thread = None

# Button mapping and color codes for display
button_map = {0: 'Left Mouse Button', 1: 'Right Mouse Button', 2: 'Middle Mouse Button', 3: 'Side Mouse 4 Button', 4: 'Side Mouse 5 Button'}
RED, GREEN, RESET = "\033[91m", "\033[92m", "\033[0m"

# Print the debug output with button states
def print_debug_output(button_states):
    debug_output = f"Port: {current_com_port} -- Baud Rate: {current_baud_rate:,}\n"
    debug_output += "---== Button States ==---\n"
    for bit, name in button_map.items():
        state = button_states.get(bit, False)
        color = GREEN if state else RED
        state_str = "Pressed" if state else "Unpressed"
        debug_output += f"{name}: {color}{state_str}{RESET}\n"
    debug_output += "---== Button States ==---"
    print("\033[H\033[J", end="")  # Clear screen
    print(debug_output)

# Open the serial port at the specified baud rate
def open_serial_port(port, baud_rate):
    try:
        return serial.Serial(port, baud_rate, timeout=1)
    except serial.SerialException as e:
        print(f"Error: Failed to open {port} at {baud_rate} baud. {str(e)}")
        return None

# Change baud rate to 4M
def change_baud_rate_to_4M():
    global makcu, current_baud_rate, is_connected
    if makcu and makcu.is_open:
        makcu.write(baud_change_command)
        makcu.flush()
        makcu.close()
        time.sleep(0.1)
        makcu = open_serial_port(makcu.name, 4000000)
        if makcu:
            current_baud_rate = 4000000
            is_connected = True
        else:
            is_connected = False

# Connect to the specified COM port
def connect_to_com_port(port):
    global makcu, is_connected, current_com_port, current_baud_rate
    if not is_connected:
        makcu = open_serial_port(port, 115200)
        if makcu:
            current_com_port, current_baud_rate = port, 115200
            change_baud_rate_to_4M()

# Close the COM port
def close_com_port():
    global makcu, is_connected
    if makcu and makcu.is_open:
        makcu.close()
        is_connected = False

# Listen to the COM port for button states
def listen_makcu():
    last_value = None
    button_states = {i: False for i in button_map} 

    while is_connected:
        try:
            if makcu.in_waiting > 0:
                byte = makcu.read(1)
                if not byte:
                    continue

                value = byte[0]
                if value != last_value:
                    byte_str = str(byte)

                    if 'b\'\\x00' in byte_str:
                        button_states = {i: False for i in button_map}
                    elif 'b\'\\x' in byte_str:
                        for bit, name in button_map.items():
                            is_pressed = bool(value & (1 << bit))
                            if is_pressed != button_states[bit]:
                                button_states[bit] = is_pressed

                    print_debug_output(button_states)
                    last_value = value

        except serial.SerialException as e:
            if "ClearCommError failed" in str(e):
                pass
            else:
                print(f"Serial error: {e}")
                break

        time.sleep(0.005)

# Find the COM port automatically
def find_com_port():
    for port in serial.tools.list_ports.comports():
        if "USB-Enhanced-SERIAL CH343" in port.description:
            return port.device
    return None

# Main function to initiate connection and start listening
def main():
    global current_com_port
    current_com_port = find_com_port()
    if current_com_port:
        connect_to_com_port(current_com_port)
        with makcu_lock:
            makcu.write(b"km.buttons(1)\r")
            makcu.flush()

        global listener_thread
        listener_thread = threading.Thread(target=listen_makcu)
        listener_thread.daemon = True
        listener_thread.start()

        while True:
            time.sleep(1)
    else:
        print("Device not found.")

# Gracefully handle keyboard interrupt
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Closing COM Port.")
        close_com_port()
        listener_thread.join()
        print("Program terminated gracefully.")

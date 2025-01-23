import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import can
import threading


def start_can_listener():
    """Function to start listening to CAN messages in a separate thread."""
    global running
    running = True
    listener_thread = threading.Thread(target=listen_to_can)
    listener_thread.daemon = True
    listener_thread.start()


def stop_can_listener():
    """Stop the CAN listener."""
    global running
    running = False
    messagebox.showinfo("Info", "CAN listener stopped.")


def listen_to_can():
    """Listens to incoming CAN messages and updates the GUI accordingly."""
    try:
        with can.interface.Bus(channel='PCAN_USBBUS1', bustype='pcan', bitrate=500000) as bus:
            while running:
                msg = bus.recv(timeout=1)  # Timeout of 1 second
                print(msg)
                if msg is not None:
                    process_can_message(msg)
    except Exception as e:
        messagebox.showerror("Error", f"CAN Error: {e}")


def process_can_message(msg):
    """Processes received CAN messages and updates the GUI."""
    global data_labels
    try:
        if msg.arbitration_id == 0x200:
            v1 = int.from_bytes(msg.data[6:8], 'big') / 1000.0
            v2 = int.from_bytes(msg.data[4:6], 'big') / 1000.0
            v3 = int.from_bytes(msg.data[2:4], 'big') / 1000.0
            v4 = int.from_bytes(msg.data[0:2], 'big') / 1000.0
            update_label(data_labels['V1'], f"{v1:.2f} V")
            update_label(data_labels['V2'], f"{v2:.2f} V")
            update_label(data_labels['V3'], f"{v3:.2f} V")
            update_label(data_labels['V4'], f"{v4:.2f} V")
        elif msg.arbitration_id == 0x204:
            temp1 = int.from_bytes(msg.data[6:8], 'big') / 10.0
            temp2 = int.from_bytes(msg.data[4:6], 'big') / 10.0
            temp3 = int.from_bytes(msg.data[2:4], 'big') / 10.0
            update_label(data_labels['T1'], f"{temp1:.1f} °C")
            update_label(data_labels['T2'], f"{temp2:.1f} °C")
            update_label(data_labels['T3'], f"{temp3:.1f} °C")
        elif msg.arbitration_id == 0x206:
            alarms = f"Alarms: {msg.data[0]:02X} {msg.data[1]:02X}"
            update_label(data_labels['Alarms'], alarms)
        elif msg.arbitration_id == 0x300:
            serial_number = ''.join(f"{byte:02X}" for byte in msg.data)
            update_label(data_labels['SN'], serial_number)
    except Exception as e:
        print(f"Error processing message: {e}")


def update_label(label, value):
    """Updates the text of a label in the GUI."""
    label.config(text=value)


def setup_gui():
    """Setup the main Tkinter GUI."""
    global data_labels

    root = tk.Tk()
    root.title("BMS Interface")

    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(main_frame, text="Battery Management System Interface", font=("Arial", 16)).grid(row=0, column=0,
                                                                                               columnspan=2, pady=10)

    # Tensions
    # ttk.Label(main_frame, text="Voltages:").grid(row=1, column=0, sticky=tk.W)
    ttk.Label(main_frame, text="V1:").grid(row=1, column=0, sticky=tk.W)
    ttk.Label(main_frame, text="V2:").grid(row=2, column=0, sticky=tk.W)
    data_labels['V1'] = ttk.Label(main_frame, text="0.00 V")
    data_labels['V1'].grid(row=1, column=1, sticky=tk.W)
    data_labels['V2'] = ttk.Label(main_frame, text="0.00 V")
    data_labels['V2'].grid(row=2, column=1, sticky=tk.W)
    data_labels['V3'] = ttk.Label(main_frame, text="0.00 V")
    data_labels['V3'].grid(row=3, column=1, sticky=tk.W)
    data_labels['V4'] = ttk.Label(main_frame, text="0.00 V")
    data_labels['V4'].grid(row=4, column=1, sticky=tk.W)

    # Temperatures
    ttk.Label(main_frame, text="Temperatures:").grid(row=5, column=0, sticky=tk.W)
    data_labels['T1'] = ttk.Label(main_frame, text="0.0 °C")
    data_labels['T1'].grid(row=5, column=1, sticky=tk.W)
    data_labels['T2'] = ttk.Label(main_frame, text="0.0 °C")
    data_labels['T2'].grid(row=6, column=1, sticky=tk.W)
    data_labels['T3'] = ttk.Label(main_frame, text="0.0 °C")
    data_labels['T3'].grid(row=7, column=1, sticky=tk.W)

    # Alarms
    ttk.Label(main_frame, text="Alarms:").grid(row=8, column=0, sticky=tk.W)
    data_labels['Alarms'] = ttk.Label(main_frame, text="None")
    data_labels['Alarms'].grid(row=8, column=1, sticky=tk.W)

    # Serial Number
    ttk.Label(main_frame, text="Serial Number:").grid(row=9, column=0, sticky=tk.W)
    data_labels['SN'] = ttk.Label(main_frame, text="N/A")
    data_labels['SN'].grid(row=9, column=1, sticky=tk.W)

    # Start/Stop Buttons
    ttk.Button(main_frame, text="Start Listening", command=start_can_listener).grid(row=10, column=0, pady=10)
    ttk.Button(main_frame, text="Stop Listening", command=stop_can_listener).grid(row=10, column=1, pady=10)

    root.mainloop()


if __name__ == "__main__":
    data_labels = {}
    running = False
    setup_gui()

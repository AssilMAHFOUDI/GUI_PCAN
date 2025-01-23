import random
import sys

# Check if tkinter is available, otherwise disable GUI
try:
    import tkinter as tk
except ImportError:
    print("Error: tkinter module is not available in this environment.")
    sys.exit("tkinter module not found")

def create_voltage_display():
    window = tk.Tk()
    window.title("Voltage Display")
    window.attributes('-fullscreen', True)
    window.configure(bg='#87CEEB')

    # Dimensions
    frame_width = 800  # Width for both frames

    # Green Frame for Voltages
    green_frame = tk.Frame(window, bg='#90EE90', padx=20, pady=10, width=frame_width, height=200)
    green_frame.place(x=20, y=20)

    voltages = ["V1", "V2", "V3", "V4", " ", " ", " ", " ", "V5", "V6", "V7", "V8", " ", " ", " ", " ", "V9", "V10", "V11", "V12", " ", " ", " ", " ", "V13"]
    voltage_values = [round(random.uniform(0, 100), 2) for v in voltages]

    for i, (voltage, value) in enumerate(zip(voltages, voltage_values)):
        label = tk.Label(green_frame, text=voltage, bg='#90EE90', fg='white', font=('Arial', 16))
        label.grid(row=i//4, column=2*i%8, padx=10)
        if voltage == " ":
            continue
        value_label = tk.Label(green_frame, text=f"{value:>5.2f}", bg='white', font=('Arial', 16))
        value_label.grid(row=i//4, column=2*i%8+1, padx=10)

    # Add 60-pixel spacing
    spacing = tk.Frame(window, height=60, bg='#87CEEB')
    spacing.place(x=20, y=green_frame.winfo_reqheight() + 40)

    # Yellow Frame for NTCs
    yellow_frame = tk.Frame(window, bg='#FFD700', padx=20, pady=10, width=frame_width, height=100)
    yellow_frame.place(x=20, y=green_frame.winfo_reqheight() + 100)  # Position below the green frame and spacing

    ntc_labels = ["NTC1", "NTC2", "NTC3"]
    ntc_values = [round(random.uniform(20, 80), 1) for _ in ntc_labels]

    for i, (ntc, value) in enumerate(zip(ntc_labels, ntc_values)):
        label = tk.Label(yellow_frame, text=ntc, bg='#FFD700', fg='black', font=('Arial', 16))
        label.grid(row=0, column=2*i, padx=10)
        value_label = tk.Label(yellow_frame, text=f"{value:>5.1f} °C", bg='white', font=('Arial', 16))
        value_label.grid(row=0, column=2*i+1, padx=10)

    # Update frame widths dynamically
    window.update_idletasks()
    yellow_frame.config(width=green_frame.winfo_width())

    window.bind('<Escape>', lambda e: window.destroy())
    window.mainloop()

create_voltage_display()

import customtkinter as ctk
import can
import threading
from tkinter import messagebox
 
class BMSInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
 
        # Global variables
        self.running = False
        self.data_labels = {}
 
        # Configure window
        self.title("Battery Management System Interface")
        self.geometry("1400x900")
 
        # Modern color scheme
        self.bg_color = '#002C66'
        self.section_colors = {
            'voltage': '#E0F4FF',
            'temperature': '#E0F4FF',
            'info': '#E0F4FF',
            'accent': '#E0F4FF'
        }
        self.text_color = '#1F2937'
        self.header_color = '#283746'
       
        # Configure appearance and color theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
 
        # Apply rounded corners and modern styling
        self.configure(fg_color=self.bg_color)
       
        self.create_main_layout()
 
    def create_main_layout(self):
        # Main frame with rounded corners
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=self.bg_color,
            corner_radius=10,
            # border_width=2,
            # border_color='#E0E0E0'
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
 
        # Modern title with accent color
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Battery Management System",
            font=('Segoe UI', 28, 'bold'),
            text_color=self.section_colors['accent']
        )
        self.title_label.pack(pady=(20, 30))
 
        # Create grid for sections with more spacing
        self.main_grid = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.bg_color,
            corner_radius=10
        )
        self.main_grid.pack(fill="both", expand=True, padx=10, pady=10)
        self.main_grid.columnconfigure((0, 1), weight=1)
 
        # Create sections with improved styling
        self.create_voltage_section()
        self.create_temperature_section()
        self.create_alarms_section()
        self.create_info_section()
        self.create_battery_stats_section()
        self.create_version_section()
        self.create_control_buttons()
 
    def create_version_section(self):
        """Add a section to display hardware and software versions."""
        # Version Section (added to info frame or as a new section)
        version_frame = ctk.CTkFrame(self.main_grid, fg_color=self.section_colors['info'])
        version_frame.grid(row=2, column=1, columnspan=1, padx=10, pady=10, sticky="nsew")
 
        ctk.CTkLabel(
            version_frame,
            text="System Versions",
            font=('Helvetica', 16, 'bold'),
            text_color=self.header_color,
            fg_color=self.section_colors['info']
        ).pack(pady=10)
 
        version_content = ctk.CTkFrame(version_frame, fg_color=self.section_colors['info'])
        version_content.pack(expand=True, fill="both", padx=10, pady=10)
 
        # Hardware Version Label
        hw_frame = ctk.CTkFrame(version_content, fg_color=self.section_colors['info'])
        hw_frame.pack(fill="x", pady=5)
       
        ctk.CTkLabel(
            hw_frame,
            text="Hardware Version:",
            fg_color=self.section_colors['info'],
            text_color=self.text_color,
            font=('Helvetica', 12)
        ).pack(side="left", padx=(0, 5))
       
        self.data_labels['HWVersion'] = ctk.CTkLabel(
            hw_frame,
            text="N/A",
            fg_color=self.section_colors['info'],
            text_color=self.text_color,
            font=('Helvetica', 12)
        )
        self.data_labels['HWVersion'].pack(side="left")
 
        # Software Version Label
        sw_frame = ctk.CTkFrame(version_content, fg_color=self.section_colors['info'])
        sw_frame.pack(fill="x", pady=5)
       
        ctk.CTkLabel(
            sw_frame,
            text="Software Version:",
            fg_color=self.section_colors['info'],
            text_color=self.text_color,
            font=('Helvetica', 12)
        ).pack(side="left", padx=(0, 5))
       
        self.data_labels['SWVersion'] = ctk.CTkLabel(
            sw_frame,
            text="N/A",
            fg_color=self.section_colors['info'],
            text_color=self.text_color,
            font=('Helvetica', 12)
        )
        self.data_labels['SWVersion'].pack(side="left")
 
 
 
    def _create_styled_section(self, parent, title, color):
        """Helper method to create consistent section styling."""
        frame = ctk.CTkFrame(
            parent,
            fg_color=color,
            corner_radius=15,
            border_width=1,
            border_color='#E0E0E0'
        )
       
        label = ctk.CTkLabel(
            frame,
            text=title,
            font=('Segoe UI', 18, 'bold'),
            # text_color=self.section_colors['accent'],
             text_color=self.header_color,
            fg_color=color
        )
        label.pack(pady=(15, 10))
       
        content_frame = ctk.CTkFrame(
            frame,
            fg_color=color,
            corner_radius=10
        )
        content_frame.pack(expand=True, fill="both", padx=15, pady=(0, 15))
       
        return frame, content_frame
 
    def create_voltage_section(self):
        voltage_frame, voltage_grid = self._create_styled_section(
            self.main_grid,
            "Voltage Measurements",
            self.section_colors['voltage']
           
        )
        voltage_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
 
        voltage_labels = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8',
                          'V9', 'V10', 'V11', 'V12', 'V13']
        for i, label_name in enumerate(voltage_labels):
            row = i // 4
            col = i % 4
            frame = ctk.CTkFrame(voltage_grid, fg_color=self.section_colors['voltage'])
            frame.grid(row=row, column=col, padx=5, pady=5, sticky="w")
           
            ctk.CTkLabel(
                frame,
                text=f"{label_name}:",
                fg_color=self.section_colors['voltage'],
                text_color=self.text_color,
                font=('Segoe UI', 12)
            ).pack(side="left", padx=(0, 5))
           
            self.data_labels[label_name] = ctk.CTkLabel(
                frame,
                text="0.00 V",
                fg_color=self.section_colors['voltage'],
                text_color=self.text_color,
                font=('Segoe UI', 12, 'bold'),
                width=100
            )
            self.data_labels[label_name].pack(side="left")
 
    # [Rest of the methods would be updated similarly with more modern styling]
    # The core logic remains the same, focusing on improved visual design
 
    def create_temperature_section(self):
        # Temperature Section
        temp_frame = ctk.CTkFrame(self.main_grid, fg_color=self.section_colors['temperature'])
        temp_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
 
        ctk.CTkLabel(
            temp_frame,
            text="Temperature Measurements",
            font=('Helvetica', 16, 'bold'),
            text_color=self.header_color,
            fg_color=self.section_colors['temperature']
        ).pack(pady=10)
 
        temp_grid = ctk.CTkFrame(temp_frame, fg_color=self.section_colors['temperature'], corner_radius=20)
        temp_grid.pack(expand=True, fill="both", padx=10, pady=10)
 
        temp_labels = ['T1', 'T2', 'T3']
        for label_name in temp_labels:
            temp_sub_frame = ctk.CTkFrame(temp_grid, fg_color=self.section_colors['temperature'])
            temp_sub_frame.pack(fill="x", pady=5)
           
            ctk.CTkLabel(
                temp_sub_frame,
                text=f"{label_name}:",
                fg_color=self.section_colors['temperature'],
                text_color=self.text_color,
                font=('Helvetica', 12)
            ).pack(side="left", padx=(0, 5))
           
            self.data_labels[label_name] = ctk.CTkLabel(
                temp_sub_frame,
                text="0.0 °C",
                fg_color=self.section_colors['temperature'],
                text_color=self.text_color,
                font=('Helvetica', 12),
                width=100
            )
            self.data_labels[label_name].pack(side="left")
 
    def create_alarms_section(self):
        # Alarms Section
        alarms_frame = ctk.CTkFrame(self.main_grid, fg_color=self.section_colors['info'])
        alarms_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
 
        ctk.CTkLabel(
            alarms_frame,
            text="Alarms",
            font=('Helvetica', 16, 'bold'),
            text_color=self.header_color,
            fg_color=self.section_colors['info']
        ).pack(pady=10)
 
        alarms_grid = ctk.CTkFrame(alarms_frame, fg_color=self.section_colors['info'])
        alarms_grid.pack(expand=True, fill="both", padx=10, pady=10)
 
        alarm_labels = ['AlarmsVMin', 'AlarmsVMax', 'AlarmsTMin', 'AlarmsTMax', 'AlarmsVBat', 'AlarmsSN']
        for i, label_name in enumerate(alarm_labels):
            row = i // 3
            col = i % 3
            frame = ctk.CTkFrame(alarms_grid, fg_color=self.section_colors['info'])
            frame.grid(row=row, column=col, padx=5, pady=5, sticky="w")
           
            ctk.CTkLabel(
                frame,
                text=f"{label_name}:",
                fg_color=self.section_colors['info'],
                text_color=self.text_color,
                font=('Helvetica', 12)
            ).pack(side="left", padx=(0, 5))
           
            self.data_labels[label_name] = ctk.CTkLabel(
                frame,
                text="0x00",
                fg_color=self.section_colors['info'],
                text_color=self.text_color,
                font=('Helvetica', 12),
                width=100
            )
            self.data_labels[label_name].pack(side="left")
 
    def create_info_section(self):
        # Additional Information Section
        info_frame = ctk.CTkFrame(self.main_grid, fg_color=self.section_colors['info'])
        info_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
 
        ctk.CTkLabel(
            info_frame,
            text="Additional Information",
            font=('Helvetica', 16, 'bold'),
            text_color=self.header_color,
            fg_color=self.section_colors['info']
        ).pack(pady=10)
 
        info_content = ctk.CTkFrame(info_frame, fg_color=self.section_colors['info'])
        info_content.pack(expand=True, fill="both", padx=10, pady=10)
 
        sn_frame = ctk.CTkFrame(info_content, fg_color=self.section_colors['info'])
        sn_frame.pack(side="left", expand=True, fill="x", padx=10)
       
        ctk.CTkLabel(
            sn_frame,
            text="Serial Number:",
            fg_color=self.section_colors['info'],
            text_color=self.text_color,
            font=('Helvetica', 12)
        ).pack(side="left", padx=(0, 5))
       
        self.data_labels['SN'] = ctk.CTkLabel(
            sn_frame,
            text="N/A",
            fg_color=self.section_colors['info'],
            text_color=self.text_color,
            font=('Helvetica', 12)
        )
        self.data_labels['SN'].pack(side="left")
 
    def create_battery_stats_section(self):
        # Battery Statistics Section
        stats_frame = ctk.CTkFrame(self.main_grid, fg_color=self.section_colors['info'])
        stats_frame.grid(row=2, column=0 ,padx=10, pady=0, sticky="nsw",columnspan=2)
 
       
        ctk.CTkLabel(
            stats_frame,
            text="  Statistiques batterie  ",
            font=('Helvetica', 16, 'bold'),
            text_color=self.header_color,
            fg_color=self.section_colors['info']
        ).pack(pady=10)
 
        stats_content = ctk.CTkFrame(stats_frame, fg_color=self.section_colors['info'])
        stats_content.pack(expand=True, fill="both", padx=10, pady=10)
 
        for stat_label in ['Vpack', 'Vmin', 'Vmax', 'Vbatt']:
            frame = ctk.CTkFrame(stats_content, fg_color=self.section_colors['info'])
            frame.pack(fill="x", pady=5)
           
            ctk.CTkLabel(
                frame,
                text=f"{stat_label}:",
                fg_color=self.section_colors['info'],
                text_color=self.text_color,
                font=('Helvetica', 12)
            ).pack(side="left", padx=(0, 5))
           
            self.data_labels[stat_label] = ctk.CTkLabel(
                frame,
                text="N/A",
                fg_color=self.section_colors['info'],
                text_color=self.text_color,
                font=('Helvetica', 12)
            )
            self.data_labels[stat_label].pack(side="left")
 
    def create_control_buttons(self):
        button_frame = ctk.CTkFrame(
            self.main_grid,
            fg_color=self.bg_color,
            corner_radius=20
        )
        button_frame.grid(row=2, column=0, padx=200)
 
        # Improved button visibility
        start_btn = ctk.CTkButton(
            button_frame,
            text="Start Listening",
            command=self.start_can_listener,
            fg_color='#4CAF50',  # Bright, clear green
            hover_color='#45a049',
            text_color='white',  # White text for contrast
            corner_radius=10,
            font=('Segoe UI', 14, 'bold'),
            width=200,  # Increased width
            height=50   # Increased height
        )
        start_btn.pack(side="left", padx=15)
 
        stop_btn = ctk.CTkButton(
            button_frame,
            text="Stop Listening",
            command=self.stop_can_listener,
            fg_color='#F44336',  # Bright, clear red
            hover_color='#D32F2F',
            text_color='white',  # White text for contrast
            corner_radius=10,
            font=('Segoe UI', 14, 'bold'),
            width=200,  # Increased width
            height=50   # Increased height
        )
        stop_btn.pack(side="left", padx=15)
    def start_can_listener(self):
        """Start listening to CAN messages in a separate thread."""
        if not self.running:
            self.running = True
            listener_thread = threading.Thread(target=self.listen_to_can)
            listener_thread.daemon = True
            listener_thread.start()
        else:
            messagebox.showinfo("Info", "CAN listener is already running.")
 
    def stop_can_listener(self):
        """Stop the CAN listener."""
        if self.running:
            self.running = False
            messagebox.showinfo("Info", "CAN listener stopped.")
        else:
            messagebox.showinfo("Info", "CAN listener is not running.")
 
    def listen_to_can(self):
        """Listen to incoming CAN messages and update the GUI."""
        try:
            with can.interface.Bus(channel='PCAN_USBBUS1', bustype='pcan', bitrate=500000) as bus:
                while self.running:
                    msg = bus.recv(timeout=1)
                    if msg is not None:
                        self.process_can_message(msg)
        except Exception as e:
            messagebox.showerror("Error", f"CAN Error: {e}")
 
    def process_can_message(self, msg):
        """Process received CAN messages and update the GUI."""
        try:
            if msg.arbitration_id == 0x200:
                for i, label_name in enumerate(['V1', 'V2', 'V3', 'V4']):
                    value = int.from_bytes(msg.data[6 - i * 2:8 - i * 2], 'big') / 1000.0
                    self.update_label(self.data_labels[label_name], f"{value:.2f} V")
            elif msg.arbitration_id == 0x201:
                for i, label_name in enumerate(['V5', 'V6', 'V7', 'V8']):
                    value = int.from_bytes(msg.data[6 - i * 2:8 - i * 2], 'big') / 1000.0
                    self.update_label(self.data_labels[label_name], f"{value:.2f} V")
            elif msg.arbitration_id == 0x202:
                for i, label_name in enumerate(['V9', 'V10', 'V11', 'V12']):
                    value = int.from_bytes(msg.data[6 - i * 2:8 - i * 2], 'big') / 1000.0
                    self.update_label(self.data_labels[label_name], f"{value:.2f} V")
            elif msg.arbitration_id == 0x203:
                v13 = int.from_bytes(msg.data[6:8], 'big') / 1000.0
                self.update_label(self.data_labels['V13'], f"{v13:.2f} V")
            elif msg.arbitration_id == 0x204:
                for i, label_name in enumerate(['T1', 'T2', 'T3']):
                    value = int.from_bytes(msg.data[6 - i * 2:8 - i * 2], 'big') / 10.0
                    self.update_label(self.data_labels[label_name], f"{value:.1f} °C")
            elif msg.arbitration_id == 0x205:
                try:
                    vpack = int.from_bytes(msg.data[0:2], 'big') / 1000.0
                    vmin = int.from_bytes(msg.data[2:4], 'big') / 1000.0
                    vmax = int.from_bytes(msg.data[4:6], 'big') / 1000.0
                    vbatt = int.from_bytes(msg.data[6:8], 'big') / 1000.0
 
                    self.update_label(self.data_labels['Vpack'], f"{vpack:.2f} V")
                    self.update_label(self.data_labels['Vmin'], f"{vmin:.2f} V")
                    self.update_label(self.data_labels['Vmax'], f"{vmax:.2f} V")
                    self.update_label(self.data_labels['Vbatt'], f"{vbatt:.2f} V")
                except Exception as e:
                    print(f"Error processing 0x205 message: {e}")
            elif msg.arbitration_id == 0x206:
                alarms = ['AlarmsVMin', 'AlarmsVMax', 'AlarmsTMin', 'AlarmsTMax', 'AlarmsVBat', 'AlarmsSN']
                for i in range(3):
                    value = int(msg.data[i])
                    value=f"{value:02X}"
                    value2=value[1]
                    value2=int(value2, 16)
                    value=value[0]
                    value=int(value, 16)
                    self.update_label(self.data_labels[alarms[2*i]], f"{value}")
                    self.update_label(self.data_labels[alarms[2*i+1]], f"{value2}")
            elif msg.arbitration_id == 0x300:
                serial_number = ''.join(f"{byte:02X}" for byte in msg.data)
                self.update_label(self.data_labels['SN'], serial_number)
            elif msg.arbitration_id == 0x301:
                # Extract Hardware Version (bytes 3-4)
                hw_version = f"{msg.data[3]}.{msg.data[4]}"
               
                # Extract Software Version (bytes 5-7)
                sw_version = f"{msg.data[5]}.{msg.data[6]}.{msg.data[7]}"
               
                # Update version labels
                self.update_label(self.data_labels['HWVersion'], hw_version)
                self.update_label(self.data_labels['SWVersion'], sw_version)
 
        except Exception as e:
            print(f"Error processing message: {e}")
 
    def update_label(self, label, value):
        """Update the text of a label in the GUI."""
        label.configure(text=value)
 
    # [Remaining methods from the original implementation would be kept the same]
    # Only visual styling is being updated
 
def main():
    app = BMSInterface()
    app.mainloop()
 
if __name__ == "__main__":
    main()
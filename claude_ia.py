import customtkinter as ctk
from tkinter import StringVar
from tkinter import messagebox

class BMSInterface(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Global variables
        self.running = False
        self.data_labels = {}

        # Configure window
        self.title("Battery Management System Interface")
        self.geometry("1200x800")

        # Color scheme
        self.bg_color = '#1E1E2F'
        self.section_colors = {
            'voltage': '#2B2B3D',
            'temperature': '#2B2B3D',
            'info': '#2B2B3D'
        }
        self.text_color = '#FFFFFF'
        self.header_color = '#00A6ED'

        # Configure appearance and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.create_main_layout()

    def create_main_layout(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Battery Management System",
            font=('Helvetica', 24, 'bold'),
            text_color=self.header_color
        )
        self.title_label.pack(pady=(0, 20))

        # Create grid for sections
        self.main_grid = ctk.CTkFrame(self.main_frame, fg_color=self.bg_color)
        self.main_grid.pack(fill="both", expand=True)
        self.main_grid.columnconfigure((0, 1, 2), weight=1)
        self.main_grid.rowconfigure((0, 1, 2), weight=1)

        # Create sections
        self.create_energy_capacity_section()
        self.create_power_capacity_section()
        self.create_battery_stats_section()
        self.create_current_power_section()
        self.create_remaining_time_section()
        self.create_transformer_section()
        self.create_battery_converter_section()

    def create_energy_capacity_section(self):
        frame = ctk.CTkFrame(self.main_grid, fg_color=self.section_colors['info'])
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            frame,
            text="Energy Capacity",
            font=('Helvetica', 16, 'bold'),
            text_color=self.header_color
        ).pack(pady=10)

        self.energy_capacity_label = ctk.CTkLabel(
            frame,
            text="371 kWh",
            font=('Helvetica', 32, 'bold'),
            text_color=self.text_color
        )
        self.energy_capacity_label.pack()

    def create_power_capacity_section(self):
        frame = ctk.CTkFrame(self.main_grid, fg_color=self.section_colors['info'])
        frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            frame,
            text="Power Capacity",
            font=('Helvetica', 16, 'bold'),
            text_color=self.header_color
        ).pack(pady=10)

        self.power_capacity_label = ctk.CTkLabel(
            frame,
            text="413 kW",
            font=('Helvetica', 32, 'bold'),
            text_color=self.text_color
        )
        self.power_capacity_label.pack()

    def create_battery_stats_section(self):
        frame = ctk.CTkFrame(self.main_grid, fg_color=self.section_colors['voltage'])
        frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            frame,
            text="Battery Stats",
            font=('Helvetica', 16, 'bold'),
            text_color=self.header_color
        ).pack(pady=10)

        stats_frame = ctk.CTkFrame(frame, fg_color=self.section_colors['voltage'])
        stats_frame.pack(fill="both", expand=True, padx=10, pady=10)

        labels = ["Bus Voltage", "State of Charge", "State of Health"]
        values = ["980 V", "80%", "95%"]
        
        for i, (label, value) in enumerate(zip(labels, values)):
            row_frame = ctk.CTkFrame(stats_frame, fg_color=self.section_colors['voltage'])
            row_frame.pack(fill="x", pady=5)

            ctk.CTkLabel(
                row_frame,
                text=f"{label}:",
                font=('Helvetica', 14),
                text_color=self.text_color
            ).pack(side="left", padx=10)

            ctk.CTkLabel(
                row_frame,
                text=value,
                font=('Helvetica', 14, 'bold'),
                text_color=self.text_color
            ).pack(side="left")

    def create_current_power_section(self):
        frame = ctk.CTkFrame(self.main_grid, fg_color=self.section_colors['info'])
        frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            frame,
            text="Current Power",
            font=('Helvetica', 16, 'bold'),
            text_color=self.header_color
        ).pack(pady=10)

        self.current_power_label = ctk.CTkLabel(
            frame,
            text="610 kW",
            font=('Helvetica', 32, 'bold'),
            text_color=self.text_color
        )
        self.current_power_label.pack()

    def create_remaining_time_section(self):
        frame = ctk.CTkFrame(self.main_grid, fg_color=self.section_colors['info'])
        frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            frame,
            text="Remaining Discharge Time",
            font=('Helvetica', 16, 'bold'),
            text_color=self.header_color
        ).pack(pady=10)

        self.remaining_time_label = ctk.CTkLabel(
            frame,
            text="4 min",
            font=('Helvetica', 32, 'bold'),
            text_color=self.text_color
        )
        self.remaining_time_label.pack()

    def create_transformer_section(self):
        frame = ctk.CTkFrame(self.main_grid, fg_color=self.section_colors['info'])
        frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            frame,
            text="Transformer",
            font=('Helvetica', 16, 'bold'),
            text_color=self.header_color
        ).pack(pady=10)

        self.transformer_label = ctk.CTkLabel(
            frame,
            text="L1: 61 °C  L2: 61 °C  L3: 58 °C",
            font=('Helvetica', 14, 'bold'),
            text_color=self.text_color
        )
        self.transformer_label.pack()

    def create_battery_converter_section(self):
        frame = ctk.CTkFrame(self.main_grid, fg_color=self.section_colors['info'])
        frame.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            frame,
            text="Battery Converter",
            font=('Helvetica', 16, 'bold'),
            text_color=self.header_color
        ).pack(pady=10)

        self.converter_label = ctk.CTkLabel(
            frame,
            text="Charge: 18 A, Discharge: 17 A",
            font=('Helvetica', 14, 'bold'),
            text_color=self.text_color
        )
        self.converter_label.pack()

def main():
    app = BMSInterface()
    app.mainloop()

if __name__ == "__main__":
    main()

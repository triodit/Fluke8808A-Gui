import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MultimeterController:
    def __init__(self, master):
        self.master = master
        self.master.title("Fluke 8808A Multimeter Controller")

        # Variable to hold the serial connection
        self.ser = None

        # Serial port selection frame
        self.port_frame = ttk.LabelFrame(self.master, text="COM Port Selection")
        self.port_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(self.port_frame, text="Select COM Port:").grid(row=0, column=0, padx=5, pady=5)
        self.combobox = ttk.Combobox(self.port_frame, values=self.get_serial_ports(), state="readonly")
        self.combobox.grid(row=0, column=1, padx=5, pady=5)

        self.connect_button = ttk.Button(self.port_frame, text="Connect", command=self.connect_port)
        self.connect_button.grid(row=0, column=2, padx=5, pady=5)

        # Measurement frame
        self.measurement_frame = ttk.LabelFrame(self.master, text="Measurements")
        self.measurement_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(self.measurement_frame, text="Measured Voltage (V):").grid(row=0, column=0, padx=5, pady=5)
        self.voltage_label = ttk.Label(self.measurement_frame, text="0.0")
        self.voltage_label.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.measurement_frame, text="Measured Current (A):").grid(row=1, column=0, padx=5, pady=5)
        self.current_label = ttk.Label(self.measurement_frame, text="0.0")
        self.current_label.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.measurement_frame, text="Measured Resistance (Ω):").grid(row=2, column=0, padx=5, pady=5)
        self.resistance_label = ttk.Label(self.measurement_frame, text="0.0")
        self.resistance_label.grid(row=2, column=1, padx=5, pady=5)

        # Graph frame
        self.graph_frame = ttk.LabelFrame(self.master, text="Real-Time Graph")
        self.graph_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.fig, self.ax = plt.subplots(3, 1, figsize=(5, 4), sharex=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        self.voltage_data = []
        self.current_data = []
        self.resistance_data = []
        self.time_data = []

        self.running = False

    def get_serial_ports(self):
        """Returns a list of available COM ports."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect_port(self):
        """Connect to the selected COM port."""
        selected_port = self.combobox.get()
        if selected_port:
            try:
                print(f"Attempting to connect to {selected_port}")
                self.ser = serial.Serial(selected_port, 9600, timeout=1)
                self.running = True
                print(f"Successfully connected to {selected_port}")
                self.update_thread = threading.Thread(target=self.update_measurements)
                self.update_thread.start()
            except serial.SerialException as e:
                print(f"Failed to connect to {selected_port}: {e}")
                messagebox.showerror("Connection Error", f"Failed to connect to {selected_port}\n{e}")
                self.ser = None

    def send_command(self, command):
        """Send SCPI command to multimeter."""
        try:
            print(f"Sending command: {command}")
            self.ser.write((command + '\n').encode())
            response = self.ser.readline().decode().strip()
            print(f"Received response: {response}")
            return response
        except Exception as e:
            print(f"Failed to send command: {command}, Error: {e}")
            messagebox.showerror("Communication Error", f"Failed to send command: {e}")
            return ""

    def update_measurements(self):
        while self.running:
            try:
                print("Updating measurements...")
                voltage = float(self.send_command("VAL1?"))  # Query primary display
                current = float(self.send_command("VAL2?"))  # Query secondary display (if applicable)
                # For example purposes, using VAL2 as current, VAL3 could be used similarly if needed.

                self.voltage_label.config(text=f"{voltage:.3f}")
                self.current_label.config(text=f"{current:.3f}")

                # Update data lists for plotting
                self.time_data.append(time.time())
                self.voltage_data.append(voltage)
                self.current_data.append(current)

                if len(self.time_data) > 100:
                    self.time_data.pop(0)
                    self.voltage_data.pop(0)
                    self.current_data.pop(0)

                self.plot_data()

                time.sleep(1)
            except Exception as e:
                print(f"Error during measurement update: {e}")
                messagebox.showerror("Update Error", f"Failed to update measurements: {e}")
                self.running = False

    def plot_data(self):
        print("Plotting data...")
        self.ax[0].clear()
        self.ax[1].clear()

        self.ax[0].plot(self.time_data, self.voltage_data, label="Voltage (V)")
        self.ax[1].plot(self.time_data, self.current_data, label="Current (A)")

        self.ax[0].set_ylabel("Voltage (V)")
        self.ax[1].set_ylabel("Current (A)")
        self.ax[1].set_xlabel("Time (s)")

        self.canvas.draw()
        print("Data plotted.")

    def close(self):
        print("Closing application...")
        self.running = False
        if self.ser:
            self.ser.close()
            print("Serial port closed.")
        self.master.quit()

# Create the main application window
root = tk.Tk()
app = MultimeterController(root)

# Ensure proper cleanup on close
root.protocol("WM_DELETE_WINDOW", app.close)
root.mainloop()

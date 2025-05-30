import serial
import time
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
# Set up the serial port configuration

serial_port = 'COM13'  # Replace with your serial port (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
baud_rate = 9600  # Set the baud rate
timeout = 1  # Set the timeout for readwing data

# Threshold value for indicator
threshold_value = 50

# Create a serial object
ser = serial.Serial(serial_port, baud_rate, timeout=timeout)

# Create the main window for the GUI
root = tk.Tk()
root.title("Predictive Maintenance of Motors")
root.geometry("800x600")

# Set color scheme (black and ash)
bg_color = "#2E2E2E"  # Ash color background
fg_color = "#FFFFFF"  # White text
highlight_color = "#FF0000"  # Red for alert

root.configure(bg=bg_color)

# Initialize data storage
data = []

# Create the figure for plotting
fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-')
ax.set_title("Real-time Data Plot", color=fg_color)
ax.set_xlabel("Time (s)", color=fg_color)
ax.set_ylabel("Value", color=fg_color)
ax.tick_params(colors=fg_color)

# Set the plot background and grid color
ax.set_facecolor(bg_color)
fig.patch.set_facecolor(bg_color)
ax.grid(True, color='gray')

# Create a canvas for matplotlib to display the plot in Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Add a label to display the received data
style = ttk.Style()
style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Arial", 14))

data_label = ttk.Label(root, text="Received Data: ")
data_label.pack(pady=10)

# Create a label for the threshold indicator
indicator_label = ttk.Label(root, text="Maintenance: Not Needed")
indicator_label.pack(pady=10)

# Create an entry widget for setting the threshold
threshold_entry_label = ttk.Label(root, text="Set Threshold Value:")
threshold_entry_label.pack(pady=5)

threshold_entry = ttk.Entry(root, font=("Arial", 14), background=bg_color, foreground=bg_color)
threshold_entry.pack(pady=5)
threshold_entry.insert(0, str(threshold_value))

# Function to update the plot
def update_plot():
    line.set_xdata(range(len(data)))
    line.set_ydata(data)
    ax.relim()
    ax.autoscale_view()
    canvas.draw()

# Function to update the GUI with serial data
def update_gui():
    while True:
        try:
            # Read a line from the serial port
            line = ser.readline().decode('utf-8').rstrip()
            if line:
                # Display the received data
                data_label.config(text=f"Temparature Measured: {line}°C")

                # Append the received value to the data list
                value = float(line)
                data.append(value)

                # Update the plot
                update_plot()

                # Check if the value exceeds the threshold
                threshold = float(threshold_entry.get())
                if value > threshold:
                    # Change the indicator to red and make it blink
                    indicator_label.config(text="Maintenance: ALERT!", foreground=highlight_color)
                else:
                    # Set the indicator to normal
                    indicator_label.config(text="Maintenance: Not Needed", foreground="green")

            time.sleep(0.1)
        except Exception as e:
            print(f"Error reading from serial: {e}")

# Start the GUI update in a separate thread to avoid blocking
thread = Thread(target=update_gui)
thread.daemon = True
thread.start()

# Run the Tkinter main loop
root.mainloop()

# Clean up the serial port
ser.close()
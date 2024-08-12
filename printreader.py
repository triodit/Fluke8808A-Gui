import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Function to check if COM200 is available
def is_com200_available():
    try:
        ser = serial.Serial('COM200')
        ser.close()
        return True
    except serial.SerialException:
        return False

# Function to read data from COM200
def read_data_from_com200():
    try:
        ser = serial.Serial('COM200', baudrate=9600, timeout=1)  # Adjust baudrate as per manual
        while True:
            data = ser.readline().decode('ascii').strip()
            if data:
                yield float(data.split()[0])  # Assuming data is in the format "6.467E-3 VDC"
    except serial.SerialException:
        print("Error reading from COM200.")
    finally:
        ser.close()

# Function to update the plot
def update_plot(frame, data_gen, xdata, ydata, line):
    y = next(data_gen)
    xdata.append(time.time())
    ydata.append(y)
    line.set_data(xdata, ydata)
    plt.xlim(xdata[0], xdata[-1] + 1)
    plt.ylim(min(ydata), max(ydata))
    return line,

# Main function to set up and start reading and plotting data
def main():
    if is_com200_available():
        print("COM200 is available. Starting to read data...")
        
        fig, ax = plt.subplots()
        xdata, ydata = [], []
        line, = ax.plot([], [], lw=2)
        
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Voltage (V)')
        ax.set_title('Real-Time Voltage Data')
        
        data_gen = read_data_from_com200()
        ani = animation.FuncAnimation(fig, update_plot, fargs=(data_gen, xdata, ydata, line), interval=1000)
        plt.show()
    else:
        print("COM200 is not available.")

if __name__ == "__main__":
    main()

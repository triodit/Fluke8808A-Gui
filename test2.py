import serial
import time
import threading

# Function to continuously listen for incoming serial data and print it
def listen_serial(ser):
    while True:
        try:
            response = ser.readline().decode('ascii').strip()
            if response:
                print(f"Received: {response}")
        except serial.SerialException as e:
            print(f"Error while reading from COM201: {e}")
            break

# Function to send commands to the serial port
def send_commands(ser):
    commands = [
        '*IDN?\n',                 # 1. Identify the instrument
        'MEASure:VOLTage?\n',      # 2. Measure voltage (first time)
        'MEASure:VOLTage?\n',      # 3. Measure voltage (second time)
        'SYST:REM\n',              # 4. Set system to remote mode
        '*IDN?\n',                 # 5. Identify the instrument again
        'VOLT:LIM?\n',             # 6. Query voltage limit
        '*IDN?\n'                  # 7. Identify the instrument again
    ]

    try:
        for command in commands:
            # Send the command
            ser.write(command.encode('ascii'))
            ser.flush()  # Ensure the command is sent immediately
            print(f"Command sent: {command.strip()}")

            # Wait 3 seconds before sending the next command
            time.sleep(3)

    except serial.SerialException as e:
        print(f"Error while sending to COM201: {e}")

def main():
    try:
        # Open the serial port with correct settings
        ser = serial.Serial(
            'COM201', 
            baudrate=115200,          # Adjust baudrate as per your device's requirements
            timeout=1,              # Timeout for read operations
            write_timeout=1,         # Timeout for write operations
            parity=serial.PARITY_NONE,   # Ensure correct parity setting
            stopbits=serial.STOPBITS_ONE, # Ensure correct stop bits setting
            bytesize=serial.EIGHTBITS     # Ensure correct byte size setting
        )
        time.sleep(2)  # Wait for the connection to establish

        # Start a thread to listen for incoming serial data
        listener_thread = threading.Thread(target=listen_serial, args=(ser,))
        listener_thread.daemon = True  # Daemonize thread to exit when main program exits
        listener_thread.start()

        # Send the commands
        send_commands(ser)

    except serial.SerialException as e:
        print(f"Error opening COM201: {e}")

    except KeyboardInterrupt:
        print("\nStopping the program.")

    finally:
        ser.close()

if __name__ == "__main__":
    main()

import serial
import time

# List of baud rates to try, based on common baud rates and the ones your device might support
baud_rates = [300, 600, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]

# Function to check if COM200 is available
def is_com200_available():
    try:
        ser = serial.Serial('COM200')
        ser.close()
        return True
    except serial.SerialException:
        return False

# Function to check if the serial connection is working in command mode at a given baud rate
def check_command_mode(baudrate):
    try:
        ser = serial.Serial('COM200', baudrate=baudrate, timeout=1)  # Set the baud rate
        time.sleep(2)  # Wait for the connection to establish

        # Example command to send (Replace with an appropriate command for your device)
        command = '*IDN?\r\n'  # Example SCPI command to query the device identification
        ser.write(command.encode('ascii'))

        # Read the response from the device
        response = ser.readline().decode('ascii').strip()

        if response:
            print(f"Baud rate {baudrate}: Received response: {response}")
            print(f"Serial connection is working at baud rate {baudrate}.")
        else:
            print(f"Baud rate {baudrate}: No response received.")
        return bool(response)

    except serial.SerialException as e:
        print(f"Baud rate {baudrate}: Error communicating with COM200: {e}")
        return False

    finally:
        ser.close()

# Main function to check serial availability and test all baud rates
def main():
    if is_com200_available():
        print("COM200 is available. Checking command mode at different baud rates...")
        for baudrate in baud_rates:
            if check_command_mode(baudrate):
                print(f"Successful communication at baud rate {baudrate}.")
                break
        else:
            print("Failed to communicate at any baud rate.")
    else:
        print("COM200 is not available.")

if __name__ == "__main__":
    main()

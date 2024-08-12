import serial

def test_fluke_communication(port, baudrate=9600, timeout=1):
    try:
        # Open the serial port
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            # Flush any existing data
            ser.flushInput()
            ser.flushOutput()

            # Send a simple test command to the multimeter
            # For example, '*IDN?' is a standard SCPI command that asks the device to identify itself
            ser.write(b'*IDN?\n')

            # Read the response from the multimeter
            response = ser.readline().decode().strip()

            # Display the response
            if response:
                print(f"Response from multimeter: {response}")
            else:
                print("No response received from the multimeter.")

    except serial.SerialException as e:
        print(f"Serial communication error: {e}")

if __name__ == "__main__":
    # Replace 'COM3' with the correct COM port your multimeter is connected to
    test_fluke_communication(port='COM200')

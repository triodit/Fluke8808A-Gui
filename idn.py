import serial

def perform_installation_test(port, baudrate=9600, timeout=1):
    try:
        # Step 1: Open serial connection
        ser = serial.Serial(port, baudrate, timeout=timeout)
        print(f"Opened serial port {port} at {baudrate} baud.")

        # Step 2: Verify that the computer interface parameters are set correctly
        # This is typically done on the multimeter itself and the software before running the script.

        # Step 4: Send the *IDN? command
        command = "*IDN?"
        ser.write((command + '\n').encode())
        print(f"Sent command: {command}")

        # Step 5: Read the response from the Meter
        response = ser.readline().decode().strip()
        print(f"Received response: {response}")

        # Step 5: Verify the response format
        if response.startswith("FLUKE, 8808A"):
            print("Test passed: Meter responded correctly.")
            print(f"Meter Identification: {response}")
        else:
            print("Test failed: Meter did not respond as expected.")
            print("Expected format: FLUKE, 8808A, nnnnnnn, n.n Dn.n")

    except serial.SerialException as e:
        print(f"Serial connection error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Step 6: Close the serial connection
        if ser.is_open:
            ser.close()
            print("Closed serial port.")

# Replace 'COMX' with the actual port (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux)
perform_installation_test('COM200')

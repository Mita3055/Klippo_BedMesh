import serial
import time

class klippo_serial:
    def __init__(self, port, baudrate=250000):
        self.port = port
        self.baudrate = baudrate
        self.connection = None

    def connect(self):
        self.connection = serial.Serial(self.port, self.baudrate, timeout=1)
        if self.connection.is_open:
            print(f"Connected to {self.port} at {self.baudrate} baud.\n")
        else:
            raise ConnectionError("Failed to connect to the printer.\n")

    def disconnect(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("Disconnected from the printer.\n")

    def writeToConsole(self, command):
        if self.connection and self.connection.is_open:
            self.connection.write(f"{command}\n".encode())
            response = self.connection.readline().decode().strip()
            return response
        else:
            raise ConnectionError("Printer is not connected.\n")
        
    def moveTo(self, x, y, z=0):
        command = f"G90\nG1 X{x} Y{y} Z{z}"
        response = self.writeToConsole(command)
        return response
    
    def home(self):
        response = self.writeToConsole("G28")
        return response
    
    def probe(self):
        if self.connection and self.connection.is_open:
            self.connection.write(b"[PROBE]\n")
            time.sleep(10) 
            lines = []

            
            while True:
                if self.connection.in_waiting > 0:
                    line = self.connection.readline().decode('utf-8').strip()
                    print(line)
                    return line
        else:
            raise ConnectionError("Printer is not connected.\n")
    
    def absolute(self):
        response = self.writeToConsole("G90")
        return response    

if __name__ == "__main__":
    # Example usage
    prnt = klippo_serial(port='COM3')  # Replace 'COM3' with your printer's port
    try:
        prnt.connect()
        response = prnt.writeToConsole('G1 X10 Y10 Z10')
        print(f"Printer response: {response}")
    finally:
        prnt.disconnect()
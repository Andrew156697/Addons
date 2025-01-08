from machine import Pin, PWM, UART
from utime import sleep, ticks_ms, ticks_diff

# Define motor states
REVERSE = 0
FORWARD = 1
BRAKE = 2

# Global variables
Up_max2 = 3000
Up_max3 = 3000
Up_max4 = 3000
first_time = False
start_state = False
pause = False
lean = 0
foot = 2000 
head = 3000
prelean = 0
prehead = 0
prefoot = 0

# UART Configuration
UART_ID = 1
BAUD_RATE = 9600
TX_PIN = 17
RX_PIN = 18
uart = UART(UART_ID, baudrate=BAUD_RATE, tx=TX_PIN, rx=RX_PIN, bits=8, parity=None, stop=1)

# Utility functions
def delay_ms(ms):
    """Custom delay function to avoid blocking."""
    start_time = ticks_ms()
    while ticks_diff(ticks_ms(), start_time) < ms:
        pass

def send_data(data):
    """Send data through UART."""
    try:
        uart.write(data)
        print(f"Sent: {data}")
    except Exception as e:
        print(f"UART send error: {e}")

def receive_data():
    """Receive data through UART."""
    try:
        if uart.any():
            data = uart.read()
            print(f"Received: {data}")
            return data
        return None
    except Exception as e:
        print(f"UART receive error: {e}")
        return None

# Motor control
def control_motor(mode, enable_pin, motor_pin1, motor_pin2):
    """Control motor operation."""
    try:
        E_pin = Pin(enable_pin, Pin.OUT)
        mp1 = Pin(motor_pin1, Pin.OUT)
        mp2 = Pin(motor_pin2, Pin.OUT)
        
        if mode == REVERSE:
            E_pin.on()
            mp1.on()
            mp2.off()
        elif mode == FORWARD:
            E_pin.on()
            mp1.off()
            mp2.on()
        else:
            E_pin.off()
            mp1.off()
            mp2.off()
    except Exception as e:
        print(f"Motor control error: {e}")

# Motor-specific control functions
def DC1_CONTROL(mode):
    control_motor(mode, 37, 41, 47)

def DC2_CONTROL(mode):
    try:
        if mode == REVERSE and DC2_STATUS() == (1, 0):
            print("DC2 at minimum position.")
            mode = BRAKE
        if mode == FORWARD and DC2_STATUS() == (0, 1):
            print("DC2 at maximum position.")
            mode = BRAKE
        control_motor(mode, 38, 42, 48)
    except Exception as e:
        print(f"DC2 control error: {e}")

def DC3_CONTROL(mode):
    try:
        if mode == REVERSE and DC3_STATUS() == (1, 0, 0):
            print("DC3 at minimum position.")
            mode = BRAKE
        if mode == FORWARD and DC3_STATUS() == (0, 0, 1):
            print("DC3 at maximum position.")
            mode = BRAKE
        control_motor(mode, 39, 2, 35)
    except Exception as e:
        print(f"DC3 control error: {e}")

def DC4_CONTROL(mode):
    try:
        if mode == REVERSE and DC4_STATUS() == (1, 0, 0):
            print("DC4 at minimum position.")
            mode = BRAKE
        if mode == FORWARD and DC4_STATUS() == (0, 0, 1):
            print("DC4 at maximum position.")
            mode = BRAKE
        control_motor(mode, 40, 1, 36)
    except Exception as e:
        print(f"DC4 control error: {e}")

# Status checking
def DC2_STATUS():
    try:
        I3 = Pin(19, Pin.IN, Pin.PULL_UP).value()
        I4 = Pin(4, Pin.IN, Pin.PULL_UP).value()
        return (I3, I4)
    except Exception as e:
        print(f"Error reading DC2 status: {e}")
        return (0, 0)

def DC3_STATUS():
    try:
        I5 = Pin(5, Pin.IN, Pin.PULL_UP).value()
        I6 = Pin(6, Pin.IN, Pin.PULL_UP).value()
        I7 = Pin(7, Pin.IN, Pin.PULL_UP).value()
        return (I5, I6, I7)
    except Exception as e:
        print(f"Error reading DC3 status: {e}")
        return (0, 0, 0)

def DC4_STATUS():
    try:
        I8 = Pin(15, Pin.IN, Pin.PULL_UP).value()
        I9 = Pin(16, Pin.IN, Pin.PULL_UP).value()
        I10 = Pin(8, Pin.IN, Pin.PULL_UP).value()
        return (I8, I9, I10)
    except Exception as e:
        print(f"Error reading DC4 status: {e}")
        return (0, 0, 0)

# Initialization and reset
def reset_all():
    """Reset all motors to a known state."""
    print("Resetting all motors...")
    DC1_CONTROL(BRAKE)
    DC2_CONTROL(BRAKE)
    DC3_CONTROL(BRAKE)
    DC4_CONTROL(BRAKE)
    delay_ms(500)
    if not reset_lo():
        print("Reset failed. Retrying...")
        reset_lo()

def reset_lo():
    """Reset limit positions."""
    global prelean, prefoot, prehead
    print("Resetting limit positions...")
    try:
        while DC3_STATUS() != (0, 1, 0) or DC2_STATUS() != (1, 0):
            DC2_CONTROL(REVERSE)
            DC3_CONTROL(REVERSE)
        prelean = prefoot = prehead = 0
        print("Reset successful.")
        return True
    except Exception as e:
        print(f"Reset error: {e}")
        return False

# Main loop
def main_loop():
    print("Starting main loop...")
    reset_all()
    while True:
        try:
            data = receive_data()
            if data:
                # Parse and handle data here
                print(f"Processing data: {data}")
            delay_ms(1000)
        except KeyboardInterrupt:
            print("Exiting program...")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")

# Start the program
if __name__ == "__main__":
    main_loop()

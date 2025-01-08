import serial
import time
import logging

response = ""
# Forward
# prefix: # | first=0/1 | pause= 0/1 | head = 0->100| foot = 0->100| lean = 0->100|  
forward_frame = "#00505050"
# state_send = False
# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

# Cấu hình cổng UART
SERIAL_PORT = '/dev/ttyAMA0'  
BAUDRATE = 9600
def send_and_wait(ser, command, expected_response, timeout=5):
    global response
    while True:
        # Gửi lệnh qua RS485
        ser.write(command.encode('utf-8'))
        logging.info(f"Sent: {command.strip()}")

        # Chờ phản hồi
        start_time = time.time()  # Bắt đầu tính thời gian
        while time.time() - start_time < timeout:
            if ser.in_waiting > 0:  # Nếu có dữ liệu trong buffer
                response = ser.readline().decode('utf-8').strip()
                logging.info(f"Received: {response}")
                if response == expected_response:  # Kiểm tra phản hồi đúng
                    return True
        logging.warning("No valid response, resending...")  # Nếu không nhận được phản hồi đúng, gửi lại lệnh


# current state --> received from


try:
    # Mở cổng serial
    ser = serial.Serial(SERIAL_PORT, baudrate=BAUDRATE, timeout=1)
    logging.info(f"Connected to {SERIAL_PORT} at {BAUDRATE} baudrate.")

    while True:
        send_and_wait(ser, forward_frame, "1:ACK_LED_ON")
        time.sleep(0.5)


except serial.SerialException as e:
    logging.error(f"Serial error: {e}")
except KeyboardInterrupt:
    logging.info("Program interrupted by user.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        logging.info("Serial port closed.")

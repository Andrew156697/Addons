import serial
import time
import logging

# Forward
start_state = 0
first_state = 0 
pause_state = 0
head = 50
foot = 60
lean = 70
prehead = 0
prefoot = 0
prelean = 0
Up_max2 = 6000
Up_max3 = 9000
Up_max4 = 5000
sum = 0

def Decode_frame(frame):
    """
    Tách 8 số sau dấu # đầu tiên từ chuỗi.

    Args:
        frame: Chuỗi chứa dữ liệu.

    Returns:
        list: Danh sách các số được tách từ chuỗi sau dấu #.
    """
    # Tìm vị trí dấu # đầu tiên
    first_hash_index = frame.find('#')
    
    if first_hash_index == -1:
        raise ValueError("Không tìm thấy dấu # trong chuỗi.")

    # Cắt chuỗi từ vị trí dấu # đầu tiên
    frame_part = frame[first_hash_index + 1:]

    # Tách chuỗi tại dấu '|'
    parts = frame_part.split('|')

    # Lấy 8 giá trị đầu tiên sau dấu #
    if len(parts) < 8:
        raise ValueError("Không có đủ 8 giá trị sau dấu #.")

    # Chuyển các phần tử thành số nguyên
    try:
        numbers = [int(part) for part in parts[:8]]
    except ValueError:
        raise ValueError("Chuỗi chứa giá trị không phải số.")

    return numbers

def combine_values(*values):
    return "#" + "|".join(map(str, values))

# prefix: # | start = 0/1 | first=0/1 | pause= 0/1 | head = 0->100| foot = 0->100| lean = 0->100| sum
# example: forward_frame = "#1|0|0|50|50|50| 151"
forward_frame = combine_values(start_state,first_state,pause_state,head,foot,lean,sum)
received_frame = combine_values(start_state,first_state, pause_state,prehead, prefoot, prelean,Up_max2,Up_max3,Up_max4)
# Receive frame
#prefix: # | first = 0/1 | pause = 0/1 | DC2: 0->100 | DC3: 0->100 | DC4: 0->100 | Umax2 | Umax3 | Umax4 | 


# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

# Cấu hình cổng UART
SERIAL_PORT = '/dev/ttyAMA0'  
BAUDRATE = 9600
def send_and_wait(ser, expected_response, timeout=4):
    global response
    while True:
        global start_state,first_state,pause_state,head,foot,lean,sum
        sum = start_state + first_state + pause_state + head + foot + lean
        forward_frame = combine_values(start_state,first_state,pause_state,head,foot,lean,sum)
        # Gửi lệnh qua RS485
        ser.write(forward_frame.encode('utf-8'))
        logging.info(f"Sent: {forward_frame.strip()}")

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
        send_and_wait(ser, forward_frame, forward_frame)
        time.sleep(0.5)


except serial.SerialException as e:
    logging.error(f"Serial error: {e}")
except KeyboardInterrupt:
    logging.info("Program interrupted by user.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        logging.info("Serial port closed.")

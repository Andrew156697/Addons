import serial
import time
import logging
import json

# Forward
start_state = 0
first_state = 0
pause_state = 0
head = 0
foot = 0
lean = 0
prehead = 0
prefoot = 0
prelean = 0
Up_max2 = 0
Up_max3 = 0
Up_max4 = 0
sum_value = 0  # Tránh dùng từ khóa Python như "sum"
old_forward_frame = ""
send_state = False
old_receive_frame = "0"
bed_parameters = "1"
# -----------------------FUNCTION-------------------
def load_options(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading options: {e}")
        return {}
def op2parameter(options_path):
    global start_state, first_state, pause_state, head, foot, lean, sum_value
    options = load_options(options_path)
    
    if((int(options.get("lean")) !=0 and int(options.get("head")) != 0 ) or (int(options.get("lean")) != 0 and int(options.get("foot")) != 0)):
        logging.info("Correct value! head - foot - lean")
    else:
        start_state = int(options.get("start_state"))
        first_state = int(options.get("first_state"))
        pause_state = int(options.get("pause_state"))
        head = int((int(options.get("head"))*Up_max2)/100)
        foot = int((int(options.get("foot"))*Up_max3)/100)
        lean = int((int(options.get("lean"))*Up_max4)/100)
        sum_value = calculate_sum(start_state, first_state, pause_state, head, foot, lean)


def Decode_frame(frame):
    # Tìm vị trí dấu # đầu tiên
    first_hash_index = frame.find('#')

    if first_hash_index == -1:
        raise ValueError("Không tìm thấy dấu # trong chuỗi.")

    # Cắt chuỗi từ vị trí dấu # đầu tiên
    frame_part = frame[first_hash_index + 1:]

    # Tách chuỗi tại dấu '|'
    parts = frame_part.split('|')

    # Lấy 8 giá trị đầu tiên sau dấu #
    if len(parts) < 9:
        raise ValueError("Không có đủ 8 giá trị sau dấu #.")

    # Chuyển các phần tử thành số nguyên
    try:
        numbers = [int(part) for part in parts[:9]]
    except ValueError:
        raise ValueError("Chuỗi chứa giá trị không phải số.")

    return numbers

def combine_values(*values):
    return "|#" + "|".join(map(str, values))

# prefix: # | start = 0/1 | first=0/1 | pause= 0/1 | head = 0->100| foot = 0->100| lean = 0->100| sum
# example: forward_frame = "#1|0|0|50|50|50| 151"
def calculate_sum(start, first, pause, head, foot, lean):
    return start + first + pause + head + foot + lean

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Cấu hình cổng UART
SERIAL_PORT = "/dev/ttyAMA0"
BAUDRATE = 9600

def send_and_wait(ser, command, expected_response, timeout=0.5):
    global start_state, first_state, pause_state, head, foot, lean, old_forward_frame, send_state, old_receive_frame, bed_parameters
    global Up_max2, Up_max3, Up_max4
    """
    Gửi lệnh qua serial và chờ phản hồi đúng trong một khoảng thời gian.
    """
    while True:
        # sum_value = calculate_sum(start_state, first_state, pause_state, head, foot, lean)
        # command = combine_values(start_state, first_state, pause_state, head, foot, lean, sum_value)
        ser.write(command.encode("utf-8"))

        if old_forward_frame != command:
            # Gửi lệnh qua RS485
            logging.info(f"Sent: {command.strip()}")
            old_forward_frame = command

        # Chờ phản hồi
        start_time = time.time()
        while time.time() - start_time < timeout:
            if ser.in_waiting > 0:  # Nếu có dữ liệu trong buffer
                response = ser.readline().decode("utf-8").strip()
                logging.info(f"Received: {response}")
                
                if old_receive_frame != bed_parameters:
                    bed_parameters = Decode_frame(response)
                    if len(bed_parameters) == 9:
                        (
                            start_state,
                            first_state, 
                            pause_state,
                            prehead, 
                            prefoot, 
                            prelean,
                            Up_max2,
                            Up_max3,
                            Up_max4
                        ) = bed_parameters
                    op2parameter("/data/options.json")
                    logging.info(f"head: {head}, lean: {lean}")
                    forward_frame = combine_values(start_state, first_state, pause_state, head, foot, lean, sum_value)
                    ser.write(forward_frame.encode("utf-8"))
                    logging.info(f"Sent: {forward_frame.strip()}")
                    old_receive_frame = bed_parameters
        
        return
                
        #         if response == expected_response:  # Kiểm tra phản hồi đúng
        #             return True
        # logging.warning("No valid response, resending...")  # Nếu không nhận được phản hồi đúng, gửi lại lệnh


try:
    # Mở cổng serial
    ser = serial.Serial(SERIAL_PORT, baudrate=BAUDRATE, timeout=0.5)
    logging.info(f"Connected to {SERIAL_PORT} at {BAUDRATE} baudrate.")

    while True:
        # Tính toán sum và khởi tạo forward_frame
        op2parameter("/data/options.json")
        forward_frame = combine_values(start_state, first_state, pause_state, head, foot, lean, sum_value)
        # if old_forward_frame != forward_frame:
            # Gửi lệnh và chờ phản hồi
        send_and_wait(ser, forward_frame, forward_frame)
            # old_forward_frame = forward_frame
        time.sleep(0.5)

except serial.SerialException as e:
    logging.error(f"Serial error: {e}")
except KeyboardInterrupt:
    logging.info("Program interrupted by user.")
finally:
    if "ser" in locals() and ser.is_open:
        ser.close()
        logging.info("Serial port closed.")
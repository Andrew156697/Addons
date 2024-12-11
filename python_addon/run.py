import cv2
import logging
from time import sleep

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

count = 0
# Mở webcam
cap = cv2.VideoCapture(0)  # 0 cho camera đầu tiên

while True:
    # Lấy từng frame
    ret, frame = cap.read()
    count += 1
    if not ret:
        logging.error("Không thể lấy frame từ camera.")
        break
    # Hiển thị thông tin trong log
    logging.info(f"Frame count: {count}, Camera read success: {ret}")
    sleep(1)

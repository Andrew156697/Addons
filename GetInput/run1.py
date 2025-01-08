import cv2
import logging
import os
from time import sleep
import mediapipe as mp

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Tắt TF_DELEGATE_OPTIONS nếu không cần thiết
os.environ["TF_DELEGATE_OPTIONS"] = "0"

# Initializing MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Open camera
camera = cv2.VideoCapture(0)
while True:
    success, frame = camera.read()
    if not success:
        logging.error("Không thể lấy frame từ camera.")
        break
    else:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)
        if results.pose_landmarks:
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                x, y, z = landmark.x, landmark.y, landmark.z  # Normalized coordinates
                logging.info(f"Landmark {idx}: x={x:.2f}, y={y:.2f}, z={z:.2f}")
            logging.info("Connected!")

    sleep(1)  # Đợi một giây trước khi lấy frame tiếp theo
camera.release()

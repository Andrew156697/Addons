import cv2
import logging
import os
from time import sleep
import mediapipe as mp

os.environ["TF_DELEGATE_OPTIONS"] = "0"

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

camera = cv2.VideoCapture(0)
while True:
    success,frame = camera.read()
    if not success:
        print("Không thể lấy frame từ camera.")
        break
    else: 
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)
        if results.pose_landmarks:
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                x, y, z = landmark.x, landmark.y, landmark.z  # Normalized coordinates
                print(f"Landmark {idx}: x={x:.2f}, y={y:.2f}, z={z:.2f}")

        sleep(1)
camera.release()

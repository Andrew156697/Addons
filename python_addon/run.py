import cv2
import logging
from time import sleep
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

camera = cv2.VideoCapture(1)
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
                x = landmark.x  # Normalized x-coordinate
                y = landmark.y  # Normalized y-coordinate
                z = landmark.z  # Depth
            print(f"Landmark {idx}: x={x:.2f}, y={y:.2f}, z={z:.2f}")
        sleep(1)
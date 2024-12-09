from flask import Flask, Response
import cv2
import time
import mediapipe as mp

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

app = Flask(__name__)

# Initialize the camera
camera = cv2.VideoCapture(0)

def generate_frames():
    frame_count = 0
    start_time = time.time()

    while True:
        # Read a frame from the camera
        success, frame = camera.read()
        if not success:
            break
        else:
            # Increment frame count
            frame_count += 1
            
            # Calculate FPS
            elapsed_time = time.time() - start_time
            if elapsed_time > 0:  # Update FPS every second
                fps = int(frame_count / elapsed_time)
                frame_count = 0
                start_time = time.time()
                
                # Put FPS text on the frame
                cv2.putText(frame, f'FPS: {fps}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Yield the frame in the correct format for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return '''
    <h1>Hello From Flask!</h1>
    <p>Visit <a href="/video_feed">/video_feed</a> to see the camera stream.</p>
    <img src="/video_feed" width="640" height="480">
    '''

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
from flask import Flask, Response
import cv2
import threading

# Flask app
app = Flask(__name__)

camera = cv2.VideoCapture(0)
frame_lock = threading.Lock()
current_frame = None

def capture_frames():
    global current_frame
    while True:
        success, frame = camera.read()
        if not success:
            break
        with frame_lock:
            current_frame = frame

@app.route('/video_feed')
def video_feed():
    def generate():
        global current_frame
        while True:
            with frame_lock:
                if current_frame is None:
                    continue
                _, buffer = cv2.imencode('.jpg', current_frame)
                frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    threading.Thread(target=capture_frames, daemon=True).start()
    app.run(host='0.0.0.0', port=8000)

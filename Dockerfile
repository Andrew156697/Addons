FROM python:3.10.12-slim


RUN apt update && apt install -y \
    python3-dev
    

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install opencv-python-headless
RUN pip install mediapipe


COPY run.py /run.py


CMD ["python", "run.py"]

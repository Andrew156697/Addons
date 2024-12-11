# Video Capture Add-on

## Mô tả
Add-on này sử dụng OpenCV để capture video từ webcam và hiển thị nó.

## Cách cài đặt
1. **Tạo Dockerfile** theo mẫu dưới đây và thay đổi `your_custom_repo` thành nơi chứa Docker image của bạn:
   ```Dockerfile
   FROM python:3.9-slim

   RUN apt-get update && apt-get install -y ffmpeg libopencv-dev && apt-get clean && rm -rf /var/lib/apt/lists/*
   WORKDIR /app
   COPY run.py /run.py
   CMD ["python", "run.py"]

# Dùng hình ảnh Python làm nền
FROM python:3.10.12-slim

# Cài đặt thư viện OpenCV và các thư viện cần thiết khác
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    libopencv-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Sao chép script Python vào container
COPY run.py /run.py

# Khởi chạy script khi container chạy
CMD ["python", "run.py"]

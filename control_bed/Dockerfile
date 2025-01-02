# Dùng hình ảnh Python làm nền
FROM python:3.10.12-slim

# Cài đặt các công cụ cần thiết cho việc biên dịch và xử lý GPIO
RUN apt update && apt install -y \
    python3-dev \
    build-essential \
    gcc \
    libgpiod-dev

# Cài đặt gpiozero và các thư viện cần thiết
RUN pip install gpiozero

# Sao chép script Python vào container
COPY run.py /run.py

CMD ["python", "run.py"]
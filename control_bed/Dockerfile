# Dùng hình ảnh Python làm nền
FROM python:3.10.12-slim

RUN apt update && apt install -y \
    python3-dev

COPY run.py .

# Cài đặt gpiozero và các thư viện cần thiết
RUN pip install gpiozero

# Sao chép script Python vào container
COPY run.py /run.py

CMD ["python", "run.py"]
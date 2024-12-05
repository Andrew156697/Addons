# Sử dụng Alpine base image
FROM alpine:latest

# Cập nhật hệ thống và cài đặt các công cụ cần thiết
RUN echo "http://dl-cdn.alpinelinux.org/alpine/v3.15/main" >> /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/v3.15/community" >> /etc/apk/repositories && \
    apk update && apk add --no-cache \
    ffmpeg \
    git \
    build-base \
    cmake \
    libjpeg-turbo-dev \
    libv4l-dev \
    linux-headers \
    gcc \
    g++ \
    make

# Tải mã nguồn mjpg-streamer và biên dịch
RUN git clone https://github.com/jacksonliam/mjpg-streamer.git && \
    cd mjpg-streamer/mjpg-streamer-experimental && \
    make && \
    make install && \
    rm -rf /var/cache/apk/* && \
    rm -rf /mjpg-streamer

# Đặt thư mục làm việc mặc định
WORKDIR /app

# Sao chép mã nguồn của bạn vào container (nếu cần)
COPY . /app

# Chạy lệnh mặc định
CMD ["sh"]

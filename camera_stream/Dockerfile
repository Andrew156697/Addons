# Sử dụng hình ảnh Alpine làm cơ sở
FROM alpine:latest

# Cập nhật và cài đặt các gói cần thiết
RUN apk update && apk add --no-cache \
    ffmpeg \
    git \
    build-base \
    cmake

# Tự biên dịch mjpg-streamer nếu không có sẵn trong kho
RUN git clone https://github.com/jacksonliam/mjpg-streamer.git && \
    cd mjpg-streamer/mjpg-streamer-experimental && \
    make && \
    make install && \
    rm -rf /var/cache/apk/* && \
    rm -rf /mjpg-streamer

# Tạo thư mục ứng dụng
WORKDIR /app

# Thêm tệp cấu hình hoặc mã nguồn vào Docker container (nếu có)
COPY . /app

# Đặt lệnh mặc định khi container chạy
CMD ["sh"]

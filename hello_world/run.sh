#!/bin/bash

# Đọc cấu hình từ file JSON
CONFIG_PATH=/data/options.json
TARGET="$(bashio::config 'target')"

# Khởi chạy dịch vụ
echo "Starting Hello World Add-on..."
echo "Target is $TARGET"



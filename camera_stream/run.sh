#!/usr/bin/with-contenv bashio

# Get camera device from configuration
CAMERA_DEVICE=$(bashio::config 'camera_device')

# Start streaming using MJPEG-Streamer
exec mjpg_streamer -i "input_uvc.so -d ${CAMERA_DEVICE} -r 640x480 -f 30" -o "output_http.so -p 8080"

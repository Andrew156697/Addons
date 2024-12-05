# Camera Stream Add-on

This add-on streams video from a connected camera and makes it available for Home Assistant.

## Configuration
- `camera_device`: Path to the camera device (default: `/dev/video0`).

## Ports
- `8080`: MJPEG stream accessible at `http://192.168.1.13:8080/`.

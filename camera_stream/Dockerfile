FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    libopencv-dev python3-opencv \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
WORKDIR /app
COPY app /app

# Install Python dependencies
RUN pip install opencv-python-headless mediapipe

# Expose Flask port
EXPOSE 5000

# Run the application
CMD ["/bin/bash", "/app/run.sh"]

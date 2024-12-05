ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.18
FROM ${BUILD_FROM}

# Install required packages
RUN apk add --no-cache ffmpeg mjpg-streamer

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

# Set default command
CMD [ "/run.sh" ]

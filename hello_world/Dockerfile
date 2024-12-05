ARG BUILD_FROM
FROM $BUILD_FROM

# Install any necessary packages (none for this simple example)
# RUN apk add --no-cache <package_name>

# Copy the run script
COPY run.sh /
RUN chmod a+x /run.sh

# Run the script when the container starts
CMD [ "/run.sh" ]
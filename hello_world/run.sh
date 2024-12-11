#!/usr/bin/with-contenv bashio
echo "Hello $(bashio::config 'name')!"
python3 -m http.server 8000
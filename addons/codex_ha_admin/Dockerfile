FROM python:3.13-alpine
ARG BUILD_VERSION
ARG BUILD_ARCH
LABEL io.hass.version="${BUILD_VERSION}" io.hass.type="addon" io.hass.arch="${BUILD_ARCH}"
RUN pip install --no-cache-dir websocket-client==1.9.0 PyYAML==6.0.3
COPY server.py /app/server.py
CMD ["python3", "-u", "/app/server.py"]

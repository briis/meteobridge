FROM mcr.microsoft.com/devcontainers/python:1-3.13

RUN apt update \
    && sudo apt install -y libpcap-dev ffmpeg vim curl jq \
    && mkdir -p /opt \
    && cd /opt \
    && git clone --depth=1 -b dev https://github.com/home-assistant/core.git hass \
    && python3 -m pip --disable-pip-version-check install --upgrade ./hass \
    && python3 -m pip install flake8 \
    && ln -s /workspaces/meteobridge/custom_components/weatherflow /opt/hass/homeassistant/components/meteobridge

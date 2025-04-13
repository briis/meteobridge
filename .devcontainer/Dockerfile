FROM mcr.microsoft.com/devcontainers/python:1-3.13

RUN apt update \
    && sudo apt install -y libpcap-dev ffmpeg vim curl jq \
    && mkdir -p /opt \
    && cd /opt \
    && git clone --depth=1 -b dev https://github.com/home-assistant/core.git hass \
    && python3 -m pip --disable-pip-version-check install --upgrade ./hass \
    && python3 -m pip install flake8

#install requirements
RUN pip3 install -r /opt/hass/requirements.txt

#copy configuration file
RUN mkdir /opt/hass/config
RUN mkdir /opt/hass/config/custom_components
COPY .devcontainer/configuration.yaml /opt/hass/config/configuration.yaml

#link to the meteobridge integration folder
RUN ln -s /workspaces/HA_Meteobridge/custom_components/meteobridge/ /opt/hass/config/custom_components/meteobridge

# Set the default shell to bash instead of sh
ENV SHELL=/bin/bash

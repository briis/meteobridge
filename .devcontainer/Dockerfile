FROM ghcr.io/home-assistant/home-assistant:2026.2

RUN pip3 install --no-cache-dir \
    flake8 \
    pymeteobridgedata \
    debugpy

RUN mkdir -p /config/custom_components

COPY .devcontainer/configuration.yaml /config/configuration.yaml

RUN ln -s /workspaces/Meteobridge/custom_components/meteobridge/ /config/custom_components/meteobridge

ENV SHELL=/bin/bash
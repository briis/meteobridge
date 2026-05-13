FROM ghcr.io/home-assistant/home-assistant:2026.2

# Optional corporate certificate
COPY .devcontainer/corp.crt* /tmp/
RUN if [ -f /tmp/corp.crt ]; then \
        cp /tmp/corp.crt /usr/local/share/ca-certificates/corp.crt && \
        update-ca-certificates; \
    fi

RUN pip3 install --no-cache-dir \
    flake8 \
    pymeteobridgedata \
    debugpy

RUN mkdir -p /config/custom_components

COPY .devcontainer/configuration.yaml /config/configuration.yaml

# Set the default shell to bash instead of sh
ENV SHELL=/bin/bash
"""Constants in meteobridge integration."""
from __future__ import annotations

from homeassistant.const import CONF_SCAN_INTERVAL

DOMAIN = "meteobridge"

METEOBRIDGE_PLATFORMS = [
    "binary_sensor",
    "sensor",
]

ATTR_UPDATED = "updated"
ATTR_BRAND = "brand"
ATTR_STATION_HW = "station_hw"
ATTR_STATION_IP = "station_ip"

CONFIG_OPTIONS = [
    CONF_SCAN_INTERVAL,
]

DEFAULT_BRAND = "Meteobridge"
DEFAULT_ATTRIBUTION = "Powered by Meteobridge"
DEFAULT_USERNAME = "meteobridge"
DEFAULT_SCAN_INTERVAL = 15

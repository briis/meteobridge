"""Constants in meteobridge integration."""
from __future__ import annotations

from homeassistant.const import CONF_SCAN_INTERVAL

DOMAIN = "meteobridge"

METEOBRIDGE_PLATFORMS = [
    "binary_sensor",
    "sensor",
]

ATTR_BRAND = "brand"
ATTR_MEASSURE_TIME = "meassure_time"
ATTR_UPDATED = "updated"

CONF_EXTRA_SENSORS = "extra_sensors"
CONFIG_OPTIONS = [
    CONF_SCAN_INTERVAL,
    CONF_EXTRA_SENSORS,
]

DEFAULT_BRAND = "Meteobridge"
DEFAULT_ATTRIBUTION = "Powered by Meteobridge"
DEFAULT_USERNAME = "meteobridge"
DEFAULT_SCAN_INTERVAL = 60

DEVICE_CLASS_LOCAL_BEAUFORT = "beaufort"
DEVICE_CLASS_LOCAL_TREND = "trend"
DEVICE_CLASS_LOCAL_UV_DESCRIPTION = "uv_description"
DEVICE_CLASS_LOCAL_WIND_CARDINAL = "wind_cardinal"

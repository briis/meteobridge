"""Constants in meteobridge integration."""
from __future__ import annotations

from homeassistant.const import CONF_SCAN_INTERVAL

DOMAIN = "meteobridge"

METEOBRIDGE_PLATFORMS = [
    "binary_sensor",
    "sensor",
]

ATTR_MEASSURE_TIME = "meassure_time"

CONF_EXTRA_SENSORS = "extra_sensors"
CONFIG_OPTIONS = [
    CONF_SCAN_INTERVAL,
    CONF_EXTRA_SENSORS,
]
CONF_UNIT_SYSTEM_IMPERIAL = "imperial"
CONF_UNIT_SYSTEM_METRIC = "metric"

DEFAULT_ATTRIBUTION = "Powered by Meteobridge"
DEFAULT_BRAND = "Meteobridge"
DEFAULT_SCAN_INTERVAL = 60
DEFAULT_USERNAME = "meteobridge"

DEVICE_CLASS_LOCAL_AQI_DESCRIPTION = "aqi_description"
DEVICE_CLASS_LOCAL_BEAUFORT = "beaufort"
DEVICE_CLASS_LOCAL_TREND = "trend"
DEVICE_CLASS_LOCAL_UV_DESCRIPTION = "uv_description"
DEVICE_CLASS_LOCAL_WIND_CARDINAL = "wind_cardinal"

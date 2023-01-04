"""Constants in meteobridge integration."""
from __future__ import annotations

from homeassistant.const import (
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_USERNAME,
)

DOMAIN = "meteobridge"

METEOBRIDGE_PLATFORMS = [
    "binary_sensor",
    "sensor",
]

ATTR_MEASSURE_TIME = "meassure_time"

CONF_EXTRA_SENSORS = "extra_sensors"
CONFIG_OPTIONS = [
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_SCAN_INTERVAL,
    CONF_EXTRA_SENSORS,
]
CONF_UNIT_SYSTEM_IMPERIAL = "imperial"
CONF_UNIT_SYSTEM_METRIC = "metric"

DEFAULT_ATTRIBUTION = "Powered by Meteobridge"
DEFAULT_BRAND = "Meteobridge"
DEFAULT_SCAN_INTERVAL = 60
DEFAULT_USERNAME = "meteobridge"

TRANSLATION_KEY_AQI_DESCRIPTION = "aqi_description"
TRANSLATION_KEY_BEAUFORT = "beaufort"
TRANSLATION_KEY_TREND = "trend"
TRANSLATION_KEY_UV_DESCRIPTION = "uv_description"
TRANSLATION_KEY_WIND_CARDINAL = "wind_cardinal"

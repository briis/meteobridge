"""Constants in mbweather component."""
import logging

from homeassistant.const import (
    CONF_UNIT_SYSTEM_METRIC,
    CONF_UNIT_SYSTEM_IMPERIAL,
)
from pymeteobridgeio import (
    DEVICE_TYPE_BINARY_SENSOR,
    DEVICE_TYPE_SENSOR,
)
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR_DOMAIN

DOMAIN = "meteobridge"

METEOBRIDGE_PLATFORMS = [
    "binary_sensor",
    "sensor",
]

DISPLAY_UNIT_SYSTEMS = [
    CONF_UNIT_SYSTEM_METRIC,
    CONF_UNIT_SYSTEM_IMPERIAL,
]

ATTR_UPDATED = "updated"
ATTR_BRAND = "brand"

DEFAULT_BRAND = "Meteobridge"
DEFAULT_ATTRIBUTION = "Data delivered by a Meteobridge powered Weather Station"
DEFAULT_USERNAME = "meteobridge"

LOGGER = logging.getLogger(__package__)

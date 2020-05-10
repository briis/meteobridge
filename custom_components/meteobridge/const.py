"""Constants in mbweather component."""
import logging

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR_DOMAIN

DOMAIN = "meteobridge"

ENTITY_ID_SENSOR_FORMAT = SENSOR_DOMAIN + "." + DOMAIN + "_{}"
ENTITY_ID_BINARY_SENSOR_FORMAT = BINARY_SENSOR_DOMAIN + "." + DOMAIN + "_{}"
ENTITY_UNIQUE_ID = DOMAIN + "_{}"

METEOBRIDGE_PLATFORMS = [
    "binary_sensor",
    "sensor",
]

DISPLAY_UNIT_SYSTEMS = [
    "metric",
    "imperial",
    "uk",
]

ATTR_UPDATED = "updated"

DEFAULT_ATTRIBUTION = "Data delivered by a Meteobridge powered Weather Station"
DEFAULT_USERNAME = "meteobridge"

LOGGER = logging.getLogger(__package__)

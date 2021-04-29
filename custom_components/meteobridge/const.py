"""Constants in meteobridge integration."""
import logging

from pymeteobridgeio import (
    DEVICE_TYPE_BINARY_SENSOR,
    DEVICE_TYPE_SENSOR,
    UNIT_TYPE_DIST_KM,
    UNIT_TYPE_DIST_MI,
    UNIT_TYPE_PRESSURE_HPA,
    UNIT_TYPE_PRESSURE_INHG,
    UNIT_TYPE_PRESSURE_MB,
    UNIT_TYPE_RAIN_MM,
    UNIT_TYPE_RAIN_IN,
    UNIT_TYPE_TEMP_CELCIUS,
    UNIT_TYPE_TEMP_FAHRENHEIT,
    UNIT_TYPE_WIND_KMH,
    UNIT_TYPE_WIND_MS,
    UNIT_TYPE_WIND_MPH,
)
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR_DOMAIN

DOMAIN = "meteobridge"

METEOBRIDGE_PLATFORMS = [
    "binary_sensor",
    "sensor",
]

TEMPERATURE_UNITS = [
    UNIT_TYPE_TEMP_CELCIUS,
    UNIT_TYPE_TEMP_FAHRENHEIT,
]

WIND_UNITS = [
    UNIT_TYPE_WIND_MS,
    UNIT_TYPE_WIND_MPH,
    UNIT_TYPE_WIND_KMH,
]

RAIN_UNITS = [
    UNIT_TYPE_RAIN_MM,
    UNIT_TYPE_RAIN_IN,
]

PRESSURE_UNITS = [
    UNIT_TYPE_PRESSURE_HPA,
    UNIT_TYPE_PRESSURE_INHG,
    UNIT_TYPE_PRESSURE_MB,
]

DISTANCE_UNITS = [
    UNIT_TYPE_DIST_KM,
    UNIT_TYPE_DIST_MI,
]

ATTR_UPDATED = "updated"
ATTR_BRAND = "brand"
ATTR_STATION_HW = "station_hw"
ATTR_STATION_IP = "station_ip"

CONF_UNIT_TEMPERATURE = "unit_temperature"
CONF_UNIT_WIND = "unit_wind"
CONF_UNIT_RAIN = "unit_rain"
CONF_UNIT_PRESSURE = "unit_pressure"
CONF_UNIT_DISTANCE = "unit_distance"
CONF_LANGUAGE = "language"
CONF_EXTRA_SENSORS = "extra_sensors"

DEFAULT_BRAND = "Meteobridge"
DEFAULT_ATTRIBUTION = "Powered by Meteobridge"
DEFAULT_USERNAME = "meteobridge"
DEFAULT_LANGUAGE = "en"
DEFAULT_SCAN_INTERVAL = 10

LOGGER = logging.getLogger(__package__)

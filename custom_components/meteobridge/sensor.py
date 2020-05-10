"""
    Support for the Meteobridge SmartEmbed
    This component will read the local weatherstation data
    and create sensors for each type.

    For a full description, go here: https://github.com/briis/mbweather

    Author: Bjarne Riis
"""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.util import slugify
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    CONF_NAME,
    CONF_UNIT_SYSTEM,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
)
from homeassistant.helpers.entity import Entity

from . import MBDATA
from .const import (
    ATTR_UPDATED,
    DOMAIN,
    DEFAULT_ATTRIBUTION,
    ENTITY_ID_SENSOR_FORMAT,
    ENTITY_UNIQUE_ID,
    DISPLAY_UNIT_SYSTEMS,
)

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    "temperature": [
        "Temperature",
        [TEMP_CELSIUS, TEMP_FAHRENHEIT, TEMP_CELSIUS],
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "temphigh": [
        "Temp High Today",
        [TEMP_CELSIUS, TEMP_FAHRENHEIT, TEMP_CELSIUS],
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "templow": [
        "Temp Low Today",
        [TEMP_CELSIUS, TEMP_FAHRENHEIT, TEMP_CELSIUS],
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "in_temperature": [
        "Indoor Temp",
        [TEMP_CELSIUS, TEMP_FAHRENHEIT, TEMP_CELSIUS],
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "dewpoint": [
        "Dewpoint",
        [TEMP_CELSIUS, TEMP_FAHRENHEIT, TEMP_CELSIUS],
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "windchill": [
        "Wind Chill",
        [TEMP_CELSIUS, TEMP_FAHRENHEIT, TEMP_CELSIUS],
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "heatindex": [
        "Heatindex",
        [TEMP_CELSIUS, TEMP_FAHRENHEIT, TEMP_CELSIUS],
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "feels_like": [
        "Feels Like",
        [TEMP_CELSIUS, TEMP_FAHRENHEIT, TEMP_CELSIUS],
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "windspeedavg": [
        "Wind Speed Avg",
        ["m/s", "mph", "km/h"],
        "mdi:weather-windy",
        None,
    ],
    "windspeed": ["Wind Speed", ["m/s", "mph", "km/h"], "mdi:weather-windy", None],
    "windbearing": ["Wind Bearing", ["°", "°", "°"], "mdi:compass-outline", None],
    "winddirection": ["Wind Direction", ["", "", ""], "mdi:compass-outline", None],
    "windgust": ["Wind Gust", ["m/s", "mph", "km/h"], "mdi:weather-windy", None],
    "raintoday": ["Rain today", ["mm", "in", "mm"], "mdi:weather-rainy", None],
    "rainrate": ["Rain rate", ["mm/h", "in/h", "mm/h"], "mdi:weather-pouring", None],
    "humidity": [
        "Humidity",
        ["%", "%", "%"],
        "mdi:water-percent",
        DEVICE_CLASS_HUMIDITY,
    ],
    "in_humidity": [
        "Indoor Hum",
        ["%", "%", "%"],
        "mdi:water-percent",
        DEVICE_CLASS_HUMIDITY,
    ],
    "pressure": [
        "Pressure",
        ["hPa", "inHg", "hPa"],
        "mdi:gauge",
        DEVICE_CLASS_PRESSURE,
    ],
    "uvindex": ["UV Index", ["UVI", "UVI", "UVI"], "mdi:weather-sunny-alert", None],
    "solarrad": [
        "Solar Radiation",
        ["W/m2", "W/m2", "W/m2"],
        "mdi:weather-sunny",
        None,
    ],
    "forecast": ["Forecast", ["", "", ""], "mdi:text-short", None],
    "temp_mmin": [
        "Temp Month Min",
        [TEMP_CELSIUS, TEMP_FAHRENHEIT, TEMP_CELSIUS],
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "temp_mmax": [
        "Temp Month Max",
        [TEMP_CELSIUS, TEMP_FAHRENHEIT, TEMP_CELSIUS],
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "temp_ymin": [
        "Temp Year Min",
        [TEMP_CELSIUS, TEMP_FAHRENHEIT, TEMP_CELSIUS],
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "temp_ymax": [
        "Temp Year Max",
        [TEMP_CELSIUS, TEMP_FAHRENHEIT, TEMP_CELSIUS],
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "windspeed_mmax": [
        "Wind Speed Month Max",
        ["m/s", "mph", "km/h"],
        "mdi:weather-windy",
        None,
    ],
    "windspeed_ymax": [
        "Wind Speed Year Max",
        ["m/s", "mph", "km/h"],
        "mdi:weather-windy",
        None,
    ],
    "rain_mmax": ["Rain Month Total", ["mm", "in", "mm"], "mdi:weather-rainy", None],
    "rain_ymax": ["Rain Year Total", ["mm", "in", "mm"], "mdi:weather-rainy", None],
    "rainrate_mmax": [
        "Rain rate Month Max",
        ["mm/h", "in/h", "mm/h"],
        "mdi:weather-pouring",
        None,
    ],
    "rainrate_ymax": [
        "Rain rate Year Max",
        ["mm/h", "in/h", "mm/h"],
        "mdi:weather-pouring",
        None,
    ],
}


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
) -> bool:
    """Set up the Meteobridge sensor platform."""
    coordinator = hass.data[MBDATA]["coordinator"]
    if not coordinator.data:
        return

    unit_system = hass.data[CONF_UNIT_SYSTEM]
    name = slugify(hass.data[CONF_NAME])

    sensors = []
    for sensor in SENSOR_TYPES:
        sensors.append(MeteobridgeSensor(coordinator, sensor, name, unit_system))
        _LOGGER.debug(f"SENSOR ADDED: {sensor}")

    async_add_entities(sensors, True)


class MeteobridgeSensor(Entity):
    """ Implementation of a SmartWeather Weatherflow Current Sensor. """

    def __init__(self, coordinator, sensor, name, unit_system):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._sensor = sensor
        self._unit_system = unit_system
        self._state = None
        self.entity_id = ENTITY_ID_SENSOR_FORMAT.format(self._sensor)
        self._name = SENSOR_TYPES[self._sensor][0]
        self._unique_id = ENTITY_UNIQUE_ID.format(slugify(self._name).replace(" ", "_"))

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self._sensor]

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        unit_system_index = DISPLAY_UNIT_SYSTEMS.index(self._unit_system)
        unit_array = SENSOR_TYPES[self._sensor][1]
        return unit_array[unit_system_index]

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return SENSOR_TYPES[self._sensor][2]

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return SENSOR_TYPES[self._sensor][3]

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        attr = {}
        attr[ATTR_ATTRIBUTION] = DEFAULT_ATTRIBUTION
        attr[ATTR_UPDATED] = self.coordinator.data["time"]

        return attr

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.coordinator.async_add_listener(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """When entity will be removed from hass."""
        self.coordinator.async_remove_listener(self.async_write_ha_state)

"""
    Support for Meteobridge SmartEmbed
    This component will read the local weatherstation data
    and create Binary sensors for each type defined below.

    For a full description, go here: https://github.com/briis/hass-mbweather

    Author: Bjarne Riis
"""
import logging
from datetime import timedelta

try:
    from homeassistant.components.binary_sensor import (
        BinarySensorEntity as BinarySensorDevice,
    )
except ImportError:
    # Prior to HA v0.110
    from homeassistant.components.binary_sensor import BinarySensorDevice

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType
from .const import (
    DOMAIN,
    DEVICE_TYPE_BINARY_SENSOR,
)

from .entity import MeteobridgeEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
) -> None:
    """Add binary sensors for Meteobridge"""
    server = hass.data[DOMAIN][entry.entry_id]["server"]
    if not server:
        return

    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    if not coordinator.data:
        return

    sensors = []
    for sensor in coordinator.data:
        if coordinator.data[sensor]["type"] == DEVICE_TYPE_BINARY_SENSOR:
            sensors.append(MeteobridgeBinarySensor(coordinator, sensor, server))
            _LOGGER.debug(f"BINARY SENSOR ADDED: {sensor}")

    async_add_entities(sensors, True)

    return True


class MeteobridgeBinarySensor(MeteobridgeEntity, BinarySensorDevice):
    """ Implementation of a Meteobridge Binary Sensor. """

    def __init__(self, coordinator, sensor, server):
        """Initialize the sensor."""
        super().__init__(coordinator, sensor, server)

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._sensor_data["value"] is True

    @property
    def icon(self):
        """Icon to use in the frontend."""
        icons = self._sensor_data["icon"].split(",")
        return f"mdi:{icons[0]}" if self.is_on else f"mdi:{icons[1]}"

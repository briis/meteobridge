"""Meteobridge Binary Sensors for Home Assistant"""

import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import (
    DOMAIN,
    DEVICE_TYPE_BINARY_SENSOR,
)

from .entity import MeteobridgeEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
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
            _LOGGER.debug("BINARY SENSOR ADDED: %s", sensor)

    async_add_entities(sensors, True)

    return True


class MeteobridgeBinarySensor(MeteobridgeEntity, BinarySensorEntity):
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

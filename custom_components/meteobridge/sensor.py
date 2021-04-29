"""Meteobridge Sensors for Home Assistant"""

import logging

from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import (
    DOMAIN,
    DEVICE_TYPE_SENSOR,
)

from .entity import MeteobridgeEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up the Meteobridge sensor platform."""
    server = hass.data[DOMAIN][entry.entry_id]["server"]
    if not server:
        return

    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    if not coordinator.data:
        return

    sensors = []
    for sensor in coordinator.data:
        if coordinator.data[sensor]["type"] == DEVICE_TYPE_SENSOR:
            sensors.append(MeteobridgeSensor(coordinator, sensor, server))
            _LOGGER.debug("SENSOR ADDED: %s", sensor)

    async_add_entities(sensors, True)

    return True


class MeteobridgeSensor(MeteobridgeEntity, Entity):
    """ Implementation of a Meteobridge Sensor. """

    def __init__(self, coordinator, sensor, server):
        """Initialize the sensor."""
        super().__init__(coordinator, sensor, server)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._sensor_data["value"]

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._sensor_data["unit"]

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return f"mdi:{self._sensor_data['icon']}"

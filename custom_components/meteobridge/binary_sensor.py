"""Meteobridge Binary Sensors for Home Assistant"""
from __future__ import annotations

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .entity import MeteobridgeEntity
from .models import MeteobridgeEntryData

_LOGGER = logging.getLogger(__name__)

BINARY_SENSOR_TYPES: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="is_freezing",
        name="Is Freezing",
        icon="mdi:snowflake-alert",
    ),
    BinarySensorEntityDescription(
        key="is_raining",
        name="Is Raining",
        icon="mdi:water-percent-alert",
    ),
    BinarySensorEntityDescription(
        key="is_lowbat",
        name="Is Battery Low",
        icon="mdi:battery-alert-variant-outline",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up sensors for UniFi Protect integration."""
    entry_data: MeteobridgeEntryData = hass.data[DOMAIN][entry.entry_id]
    meteobridgeapi = entry_data.meteobridgeapi
    coordinator = entry_data.coordinator
    device_data = entry_data.device_data

    entities = []
    for description in BINARY_SENSOR_TYPES:
        entities.append(
            MeteobridgeBinarySensor(
                meteobridgeapi,
                coordinator,
                device_data,
                description,
                entry,
            )
        )

        _LOGGER.debug(
            "Adding binary sensor entity %s",
            description.name,
        )

    async_add_entities(entities)


class MeteobridgeBinarySensor(MeteobridgeEntity, BinarySensorEntity):
    """Implementation of a Meteobridge Binary Sensor."""

    def __init__(
        self,
        meteobridgeapi,
        coordinator,
        device_data,
        description: BinarySensorEntityDescription,
        entries: ConfigEntry,
    ):
        """Initialize an WeatherFlow binary sensor."""
        super().__init__(
            meteobridgeapi,
            coordinator,
            device_data,
            description,
            entries,
        )
        self._attr_name = f"{DOMAIN.capitalize()} {self.entity_description.name}"

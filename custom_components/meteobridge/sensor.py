"""Meteobridge Sensors for Home Assistant"""
from __future__ import annotations

import logging
from dataclasses import dataclass

from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    DEGREE,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_TIMESTAMP,
    DEVICE_CLASS_VOLTAGE,
    TEMP_CELSIUS,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import StateType

from .const import (
    DOMAIN,
    DEVICE_CLASS_LOCAL_BEAUFORT,
    DEVICE_CLASS_LOCAL_TREND,
    DEVICE_CLASS_LOCAL_WIND_CARDINAL,
)
from .entity import MeteobridgeEntity
from .models import MeteobridgeEntryData


@dataclass
class MeteobridgeRequiredKeysMixin:
    """Mixin for required keys."""

    unit_type: str
    always_add: bool


@dataclass
class MeteobridgeSensorEntityDescription(
    SensorEntityDescription, MeteobridgeRequiredKeysMixin
):
    """Describes Meteobridge Sensor entity."""


SENSOR_TYPES: tuple[MeteobridgeSensorEntityDescription, ...] = (
    MeteobridgeSensorEntityDescription(
        key="temperature",
        name="Temperature",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        always_add=True,
    ),
    MeteobridgeSensorEntityDescription(
        key="pressure",
        name="Sealevel Pressure",
        device_class=DEVICE_CLASS_PRESSURE,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="pressure",
        always_add=True,
    ),
    MeteobridgeSensorEntityDescription(
        key="rainrate",
        name="Precipitation Rate",
        icon="mdi:weather-pouring",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="precipitation_rate",
        always_add=False,
    ),
    MeteobridgeSensorEntityDescription(
        key="temperature_2",
        name="Temperature Sensor 2",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        always_add=False,
    ),
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up sensors for Meteobridge integration."""
    entry_data: MeteobridgeEntryData = hass.data[DOMAIN][entry.entry_id]
    meteobridgeapi = entry_data.meteobridgeapi
    coordinator = entry_data.coordinator
    device_data = entry_data.device_data
    unit_descriptions = entry_data.unit_descriptions

    entities = []
    for description in SENSOR_TYPES:
        if description.always_add or (
            getattr(coordinator.data, description.key) is not None
        ):
            entities.append(
                MeteobridgeSensor(
                    meteobridgeapi,
                    coordinator,
                    device_data,
                    description,
                    entry,
                    unit_descriptions,
                )
            )

            _LOGGER.debug(
                "Adding sensor entity %s",
                description.name,
            )

    async_add_entities(entities)


class MeteobridgeSensor(MeteobridgeEntity, SensorEntity):
    """Implementation of a Meteobridge Sensor."""

    def __init__(
        self,
        meteobridgeapi,
        coordinator,
        device_data,
        description,
        entries: ConfigEntry,
        unit_descriptions,
    ):
        """Initialize an Meteobridge sensor."""
        super().__init__(
            meteobridgeapi,
            coordinator,
            device_data,
            description,
            entries,
        )
        self._attr_name = f"{DOMAIN.capitalize()} {self.entity_description.name}"
        if self.entity_description.native_unit_of_measurement is None:
            self._attr_native_unit_of_measurement = unit_descriptions[
                self.entity_description.unit_type
            ]

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""

        return (
            getattr(self.coordinator.data, self.entity_description.key)
            if self.coordinator.data
            else None
        )

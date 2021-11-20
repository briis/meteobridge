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
    DEVICE_CLASS_PM1,
    DEVICE_CLASS_PM10,
    DEVICE_CLASS_PM25,
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
        key="windchill",
        name="Wind Chill",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        always_add=True,
    ),
    MeteobridgeSensorEntityDescription(
        key="heatindex",
        name="Heat Index",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        always_add=True,
    ),
    MeteobridgeSensorEntityDescription(
        key="air_pollution",
        name="Air Quality PM10",
        device_class=DEVICE_CLASS_PM10,
        state_class=STATE_CLASS_MEASUREMENT,
        native_unit_of_measurement="µg/m³",
        unit_type="none",
        always_add=False,
    ),
    MeteobridgeSensorEntityDescription(
        key="air_pm_25",
        name="Air Quality PM2.5",
        device_class=DEVICE_CLASS_PM25,
        state_class=STATE_CLASS_MEASUREMENT,
        native_unit_of_measurement="µg/m³",
        unit_type="none",
        always_add=False,
    ),
    MeteobridgeSensorEntityDescription(
        key="air_pm_1",
        name="Air Quality PM1",
        device_class=DEVICE_CLASS_PM1,
        state_class=STATE_CLASS_MEASUREMENT,
        native_unit_of_measurement="µg/m³",
        unit_type="none",
        always_add=False,
    ),
    MeteobridgeSensorEntityDescription(
        key="humidity",
        name="Relative Humidity",
        device_class=DEVICE_CLASS_HUMIDITY,
        state_class=STATE_CLASS_MEASUREMENT,
        native_unit_of_measurement="%",
        unit_type="none",
        always_add=True,
    ),
    MeteobridgeSensorEntityDescription(
        key="windspeedavg",
        name="Wind Speed Avg.",
        icon="mdi:weather-windy-variant",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="length",
        always_add=True,
    ),
    MeteobridgeSensorEntityDescription(
        key="windgust",
        name="Wind Gust",
        icon="mdi:weather-windy",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="length",
        always_add=True,
    ),
    MeteobridgeSensorEntityDescription(
        key="windbearing",
        name="Wind Direction",
        icon="mdi:compass",
        native_unit_of_measurement=DEGREE,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        always_add=True,
    ),
    MeteobridgeSensorEntityDescription(
        key="wind_cardinal",
        name="Wind Cardinal",
        icon="mdi:compass",
        device_class=DEVICE_CLASS_LOCAL_WIND_CARDINAL,
        unit_type="none",
        always_add=True,
    ),
    MeteobridgeSensorEntityDescription(
        key="raintoday",
        name="Precipitation Today",
        icon="mdi:weather-rainy",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="precipitation",
        always_add=True,
    ),
    MeteobridgeSensorEntityDescription(
        key="rainrate",
        name="Precipitation Rate",
        icon="mdi:weather-pouring",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="precipitation_rate",
        always_add=True,
    ),
    MeteobridgeSensorEntityDescription(
        key="dewpoint",
        name="Dewpoint",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        always_add=True,
    ),
    MeteobridgeSensorEntityDescription(
        key="in_temperature",
        name="Inhouse Temperature",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        always_add=True,
    ),
    MeteobridgeSensorEntityDescription(
        key="in_humidity",
        name="Inhouse Humidity",
        device_class=DEVICE_CLASS_HUMIDITY,
        state_class=STATE_CLASS_MEASUREMENT,
        native_unit_of_measurement="%",
        unit_type="none",
        always_add=True,
    ),
    MeteobridgeSensorEntityDescription(
        key="bft_value",
        name="Beaufort",
        icon="mdi:windsock",
        native_unit_of_measurement="Bft",
        state_class=STATE_CLASS_MEASUREMENT,
        unit_type="none",
        always_add=True,
    ),
    MeteobridgeSensorEntityDescription(
        key="beaufort_description",
        name="Beaufort Description",
        icon="mdi:windsock",
        device_class=DEVICE_CLASS_LOCAL_BEAUFORT,
        unit_type="none",
        always_add=True,
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

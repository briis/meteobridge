"""Meteobridge Platform"""
from __future__ import annotations

import logging
from datetime import timedelta

import homeassistant.helpers.device_registry as dr
from aiohttp.client_exceptions import ServerDisconnectedError
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_USERNAME,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util.unit_system import (
    METRIC_SYSTEM,
)

from pymeteobridgedata import BadRequest, Invalid, MeteobridgeApiClient, NotAuthorized
from pymeteobridgedata.data import DataLoggerDescription, ObservationDescription

from .const import (
    CONF_EXTRA_SENSORS,
    CONFIG_OPTIONS,
    CONF_UNIT_SYSTEM_IMPERIAL,
    CONF_UNIT_SYSTEM_METRIC,
    DEFAULT_BRAND,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    METEOBRIDGE_PLATFORMS,
)
from .models import MeteobridgeEntryData

_LOGGER = logging.getLogger(__name__)


@callback
def _async_import_options_from_data_if_missing(hass: HomeAssistant, entry: ConfigEntry):
    options = dict(entry.options)
    data = dict(entry.data)
    modified = False
    for importable_option in CONFIG_OPTIONS:
        if importable_option not in entry.options and importable_option in entry.data:
            options[importable_option] = entry.data[importable_option]
            del data[importable_option]
            modified = True

    if modified:
        hass.config_entries.async_update_entry(entry, data=data, options=options)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Meteobridge config entries."""
    _async_import_options_from_data_if_missing(hass, entry)

    session = async_create_clientsession(hass)
    unit_system = (
        CONF_UNIT_SYSTEM_METRIC
        if hass.config.units is METRIC_SYSTEM
        else CONF_UNIT_SYSTEM_IMPERIAL
    )

    meteobridgeapi = MeteobridgeApiClient(
        entry.options[CONF_USERNAME],
        entry.options[CONF_PASSWORD],
        entry.data[CONF_HOST],
        extra_sensors=entry.options[CONF_EXTRA_SENSORS],
        units=unit_system,
        session=session,
    )

    try:
        await meteobridgeapi.initialize()
        device_data: DataLoggerDescription = meteobridgeapi.device_data
        if device_data is not None:
            _LOGGER.debug("Connected to Meteobridge Platform %s", device_data.station)

    except NotAuthorized:
        _LOGGER.error(
            "Authorize failure at Meteobridge Server. Please reinstall integration."
        )
        return False
    except (BadRequest, ServerDisconnectedError) as notreadyerror:
        _LOGGER.warning(str(notreadyerror))
        raise ConfigEntryNotReady from notreadyerror

    if entry.unique_id is None:
        hass.config_entries.async_update_entry(entry, unique_id=device_data.key)

    async def async_update_data():
        """Obtain the latest data from Meteobridge."""
        try:
            data: ObservationDescription = await meteobridgeapi.update_observations()
            return data

        except (BadRequest, Invalid) as err:
            raise UpdateFailed(f"Error while retreiving data: {err}") from err

    unit_descriptions = await meteobridgeapi.load_unit_system()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(
            seconds=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        ),
    )
    await coordinator.async_config_entry_first_refresh()
    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = MeteobridgeEntryData(
        coordinator=coordinator,
        meteobridgeapi=meteobridgeapi,
        device_data=device_data,
        unit_descriptions=unit_descriptions,
    )

    await _async_get_or_create_nvr_device_in_registry(hass, entry, device_data)

    hass.config_entries.async_setup_platforms(entry, METEOBRIDGE_PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_options_updated))

    return True


async def _async_get_or_create_nvr_device_in_registry(
    hass: HomeAssistant, entry: ConfigEntry, device_data: DataLoggerDescription
) -> None:
    device_registry = dr.async_get(hass)

    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        connections={(dr.CONNECTION_NETWORK_MAC, entry.unique_id)},
        identifiers={(DOMAIN, entry.unique_id)},
        manufacturer=DEFAULT_BRAND,
        name=f"{device_data.station} ({device_data.ip})",
        model=device_data.platform,
        sw_version=device_data.swversion,
    )


async def _async_options_updated(hass: HomeAssistant, entry: ConfigEntry):
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload WeatherFlow entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, METEOBRIDGE_PLATFORMS
    )
    return unload_ok

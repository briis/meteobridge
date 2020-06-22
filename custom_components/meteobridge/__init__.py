"""Meteobridge Integration for Home Assistant"""
import asyncio
import logging
from datetime import timedelta

import homeassistant.helpers.device_registry as dr
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (CONF_HOST, CONF_ID, CONF_PASSWORD,
                                 CONF_SCAN_INTERVAL, CONF_UNIT_SYSTEM,
                                 CONF_UNIT_SYSTEM_IMPERIAL,
                                 CONF_UNIT_SYSTEM_METRIC, CONF_USERNAME)
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.dispatcher import (async_dispatcher_connect,
                                              async_dispatcher_send)
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.typing import ConfigType, HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pymeteobridgeio import InvalidCredentials, Meteobridge, ResultError

from .const import (CONF_LANGUAGE, DEFAULT_ATTRIBUTION, DEFAULT_BRAND,
                    DEFAULT_LANGUAGE, DEFAULT_SCAN_INTERVAL, DOMAIN,
                    METEOBRIDGE_PLATFORMS)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=10)


async def async_setup(hass: HomeAssistantType, config: ConfigType) -> bool:
    """Set up configured Meteobridge."""

    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    """Set up Meteobridge platforms as config entry."""

    if not entry.options:
        hass.config_entries.async_update_entry(
            entry,
            options={
                CONF_SCAN_INTERVAL: entry.data.get(
                    CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                ),
                CONF_LANGUAGE: entry.data.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
            },
        )

    unit_system = (
        CONF_UNIT_SYSTEM_METRIC
        if hass.config.units.is_metric
        else CONF_UNIT_SYSTEM_IMPERIAL
    )
    session = async_get_clientsession(hass)

    mb_server = Meteobridge(
        entry.data[CONF_HOST],
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD],
        unit_system,
        entry.options.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
        session,
    )
    _LOGGER.debug("Connected to Meteobridge Platform")

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = mb_server

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=mb_server.get_sensor_data,
        update_interval=timedelta(
            seconds=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        ),
    )

    try:
        svr_info = await mb_server.get_server_data()
    except InvalidCredentials:
        _LOGGER.error(
            "Could not Authorize against Meteobridge Server. Please reinstall integration."
        )
        return
    except ResultError:
        raise ConfigEntryNotReady

    await coordinator.async_refresh()
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "mb": mb_server,
        "server": svr_info,
    }

    await _async_get_or_create_meteobridge_device_in_registry(hass, entry, svr_info)

    for platform in METEOBRIDGE_PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    if not entry.update_listeners:
        entry.add_update_listener(async_update_options)

    return True


async def _async_get_or_create_meteobridge_device_in_registry(
    hass: HomeAssistantType, entry: ConfigEntry, svr
) -> None:
    device_registry = await dr.async_get_registry(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        connections={(dr.CONNECTION_NETWORK_MAC, svr["mac_address"])},
        identifiers={(DOMAIN, svr["mac_address"])},
        manufacturer=DEFAULT_BRAND,
        name=entry.data[CONF_HOST],
        model=svr["platform_hw"],
        sw_version=svr["swversion"],
    )


async def async_update_options(hass: HomeAssistantType, entry: ConfigEntry):
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    """Unload Unifi Protect config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in METEOBRIDGE_PLATFORMS
            ]
        )
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

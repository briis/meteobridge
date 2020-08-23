"""Meteobridge Integration for Home Assistant"""
import asyncio
import logging
from datetime import timedelta

import homeassistant.helpers.device_registry as dr
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    CONF_ID,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_USERNAME,
)
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from aiohttp.client_exceptions import ServerDisconnectedError
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.typing import ConfigType, HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pymeteobridgeio import (
    Meteobridge,
    InvalidCredentials,
    RequestError,
    ResultError,
)

from .const import (
    CONF_LANGUAGE,
    CONF_EXTRA_SENSORS,
    CONF_UNIT_TEMPERATURE,
    CONF_UNIT_WIND,
    CONF_UNIT_RAIN,
    CONF_UNIT_PRESSURE,
    CONF_UNIT_DISTANCE,
    DEFAULT_ATTRIBUTION,
    DEFAULT_BRAND,
    DEFAULT_LANGUAGE,
    DEFAULT_SCAN_INTERVAL,
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
    DOMAIN,
    METEOBRIDGE_PLATFORMS,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=10)


async def async_setup(hass: HomeAssistantType, config: ConfigType) -> bool:
    """Set up configured Meteobridge."""

    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    """Set up Meteobridge platforms as config entry."""

    if hass.config.units.is_metric:
        _unit_temperature = UNIT_TYPE_TEMP_CELCIUS
        _unit_wind = UNIT_TYPE_WIND_MS
        _unit_rain = UNIT_TYPE_RAIN_MM
        _unit_pressure = UNIT_TYPE_PRESSURE_HPA
        _unit_distance = UNIT_TYPE_DIST_KM
    else:
        _unit_temperature = UNIT_TYPE_TEMP_FAHRENHEIT
        _unit_wind = UNIT_TYPE_WIND_MPH
        _unit_rain = UNIT_TYPE_RAIN_IN
        _unit_pressure = UNIT_TYPE_PRESSURE_INHG
        _unit_distance = UNIT_TYPE_DIST_MI

    if not entry.options:
        hass.config_entries.async_update_entry(
            entry,
            options={
                CONF_UNIT_TEMPERATURE: entry.data.get(
                    CONF_UNIT_TEMPERATURE, _unit_temperature
                ),
                CONF_UNIT_WIND: entry.data.get(CONF_UNIT_WIND, _unit_wind),
                CONF_UNIT_RAIN: entry.data.get(CONF_UNIT_RAIN, _unit_rain),
                CONF_UNIT_PRESSURE: entry.data.get(CONF_UNIT_PRESSURE, _unit_pressure),
                CONF_UNIT_DISTANCE: entry.data.get(CONF_UNIT_DISTANCE, _unit_distance),
                CONF_EXTRA_SENSORS: entry.data.get(CONF_EXTRA_SENSORS, 0),
                CONF_SCAN_INTERVAL: entry.data.get(
                    CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                ),
                CONF_LANGUAGE: entry.data.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
            },
        )

    session = async_get_clientsession(hass)

    mb_server = Meteobridge(
        entry.data[CONF_HOST],
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD],
        entry.options.get(CONF_UNIT_TEMPERATURE, _unit_temperature),
        entry.options.get(CONF_UNIT_WIND, _unit_wind),
        entry.options.get(CONF_UNIT_RAIN, _unit_rain),
        entry.options.get(CONF_UNIT_PRESSURE, _unit_pressure),
        entry.options.get(CONF_UNIT_DISTANCE, _unit_distance),
        entry.options.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
        entry.options.get(CONF_EXTRA_SENSORS, 0),
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
    except (ResultError, ServerDisconnectedError) as err:
        _LOGGER.warning(str(err))
        raise ConfigEntryNotReady
    except RequestError as err:
        _LOGGER.error(f"Error occured: {err}")
        return

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

"""Meteobridge Weather Integration for Home Assistant"""
import logging
from datetime import timedelta, datetime
import voluptuous as vol

from homeassistant.const import (
    CONF_NAME,
    CONF_HOST,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_UNIT_SYSTEM,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers import update_coordinator

from .config_flow import meteobridge_hosts
from pymeteobridgeio import Meteobridge, UnexpectedError
from .const import (
    DOMAIN,
    DEFAULT_ATTRIBUTION,
    METEOBRIDGE_PLATFORMS,
)

_LOGGER = logging.getLogger(__name__)

MBDATA = DOMAIN

DEFAULT_SCAN_INTERVAL = timedelta(seconds=10)


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Set up configured Meteobridge."""
    # We allow setup only through config flow type of config
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Meteobridge platforms as config entry."""

    unit_system = config_entry.data[CONF_UNIT_SYSTEM]
    session = async_get_clientsession(hass)

    mb_server = Meteobridge(
        session,
        config_entry.data[CONF_HOST],
        config_entry.data[CONF_USERNAME],
        config_entry.data[CONF_PASSWORD],
        unit_system,
    )
    _LOGGER.debug("Connected to Meteobridge Platform")

    hass.data[CONF_NAME] = config_entry.data[CONF_NAME]
    hass.data[CONF_UNIT_SYSTEM] = unit_system

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=mb_server.update,
        update_interval=DEFAULT_SCAN_INTERVAL,
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()
    hass.data[MBDATA] = {
        "coordinator": coordinator,
        "mb": mb_server,
    }

    for platform in METEOBRIDGE_PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(config_entry, platform)
        )
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    for platform in METEOBRIDGE_PLATFORMS:
        await hass.config_entries.async_forward_entry_unload(config_entry, platform)
    return True

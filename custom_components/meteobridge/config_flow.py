"""Config flow to configure Meteobridge Integration."""
from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import (
    CONF_HOST,
    CONF_ID,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_USERNAME,
)
from homeassistant.core import callback
from homeassistant.helpers import aiohttp_client
from pymeteobridgedata import BadRequest, MeteobridgeApiClient, NotAuthorized
from pymeteobridgedata.data import DataLoggerDescription

from .const import DEFAULT_SCAN_INTERVAL, DEFAULT_USERNAME, DOMAIN

_LOGGER = logging.getLogger(__name__)


class MeteobridgeFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a Meteobridge config flow."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        if user_input is None:
            return await self._show_setup_form(user_input)

        errors = {}

        session = aiohttp_client.async_get_clientsession(self.hass)

        meteobridge = MeteobridgeApiClient(
            user_input[CONF_USERNAME],
            user_input[CONF_PASSWORD],
            user_input[CONF_HOST],
            session=session,
        )

        try:
            await meteobridge.initialize()

            device_data: DataLoggerDescription = meteobridge.device_data

        except NotAuthorized:
            errors["base"] = "invalid_credentials"
            return await self._show_setup_form(errors)
        except BadRequest:
            errors["base"] = "host_not_found"
            return await self._show_setup_form(errors)

        await self.async_set_unique_id(device_data.key)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=f"{device_data.platform} ({user_input[CONF_HOST]})",
            data={
                CONF_ID: device_data.key,
                CONF_HOST: user_input[CONF_HOST],
                CONF_USERNAME: user_input.get(CONF_USERNAME),
                CONF_PASSWORD: user_input.get(CONF_PASSWORD),
            },
            options={
                CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
            },
        )

    async def _show_setup_form(self, errors=None):
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_USERNAME, default=DEFAULT_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors or {},
        )


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.data.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=10, max=60)),
                }
            ),
        )

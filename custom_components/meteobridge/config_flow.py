"""Config flow to configure MBWeather Integration."""
import logging

from pymeteobridgeio import (
    Meteobridge,
    InvalidCredentials,
    RequestError,
    ResultError,
)

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_ID,
    CONF_HOST,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_UNIT_SYSTEM_METRIC,
    CONF_UNIT_SYSTEM_IMPERIAL,
)
from homeassistant.config_entries import ConfigFlow
from homeassistant.helpers import aiohttp_client

from .const import (
    DOMAIN,
    DEFAULT_USERNAME,
    DISPLAY_UNIT_SYSTEMS,
)

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class MeteobridgeFlowHandler(ConfigFlow):
    """Handle a Meteobridge config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def _show_setup_form(self, errors=None):
        """Show the setup form to the user."""

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_USERNAME, default="meteobridge"): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors or {},
        )

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        if user_input is None:
            return await self._show_setup_form(user_input)

        _unit_system = (
            CONF_UNIT_SYSTEM_METRIC
            if self.hass.config.units.is_metric
            else CONF_UNIT_SYSTEM_IMPERIAL
        )
        errors = {}

        session = aiohttp_client.async_get_clientsession(self.hass)
        mb_server = Meteobridge(
            user_input[CONF_HOST],
            user_input[CONF_USERNAME],
            user_input[CONF_PASSWORD],
            _unit_system,
            session,
        )

        try:
            data = await mb_server.get_server_data()
            unique_id = data["mac_address"]
            platform_hw = data["platform_hw"]
        except InvalidCredentials:
            errors["base"] = "invalid_credentials"
            return await self._show_setup_form(errors)
        except ResultError:
            errors["base"] = "host_not_found"
            return await self._show_setup_form(errors)

        entries = self._async_current_entries()
        for entry in entries:
            if entry.data[CONF_ID] == unique_id:
                return self.async_abort(reason="mac_exists")

        return self.async_create_entry(
            title=f"{platform_hw} ({user_input[CONF_HOST]})",
            data={
                CONF_ID: unique_id,
                CONF_HOST: user_input[CONF_HOST],
                CONF_USERNAME: user_input.get(CONF_USERNAME),
                CONF_PASSWORD: user_input.get(CONF_PASSWORD),
            },
        )

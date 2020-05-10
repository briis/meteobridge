"""Config flow to configure MBWeather Integration."""
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_HOST,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_NAME,
    CONF_UNIT_SYSTEM,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import aiohttp_client
import homeassistant.helpers.config_validation as cv
from homeassistant.util import slugify

from pymeteobridgeio import Meteobridge, UnexpectedError
from .const import (
    DOMAIN,
    DEFAULT_USERNAME,
    DISPLAY_UNIT_SYSTEMS,
)


@callback
def meteobridge_hosts(hass: HomeAssistant):
    """Return configurations of MBWeather component."""
    return {
        (slugify(entry.data[CONF_HOST]))
        for entry in hass.config_entries.async_entries(DOMAIN)
    }


@config_entries.HANDLERS.register(DOMAIN)
class MeteobridgeFlowHandler(config_entries.ConfigFlow):
    """Config flow for MBWeather component."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self) -> None:
        """Initialize MBWeather configuration flow."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            is_ok = await self._check_ip_address(
                user_input[CONF_HOST],
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD],
            )
            if is_ok:
                host = slugify(user_input[CONF_HOST])
                if not self._host_in_configuration_exists(host):
                    return self.async_create_entry(
                        title=user_input[CONF_HOST], data=user_input
                    )

                self._errors[CONF_HOST] = "ip_exists"
            else:
                self._errors["base"] = "host_not_found"

        # Fill in default values in form
        if not meteobridge_hosts(self.hass):
            return await self._show_config_form(username=DEFAULT_USERNAME, name=DOMAIN)

        return await self._show_config_form()

    def _host_in_configuration_exists(self, host: str) -> bool:
        """Return True if host exists in configuration."""
        if host in meteobridge_hosts(self.hass):
            return True
        return False

    async def _show_config_form(self, username: str = None, name: str = None):
        """Show the configuration form to edit station data."""
        _unit_system = "metric" if self.hass.config.units.is_metric else "imperial"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_USERNAME, default=username): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_NAME, default=name): str,
                    vol.Required(CONF_UNIT_SYSTEM, default=_unit_system): vol.In(
                        DISPLAY_UNIT_SYSTEMS
                    ),
                }
            ),
            errors=self._errors,
        )

    async def _check_ip_address(self, host: str, username: str, password: str) -> bool:
        """Return true if Meteobridge responds."""

        try:
            unit_system = "metric" if self.hass.config.units.is_metric else "imperial"
            session = aiohttp_client.async_get_clientsession(self.hass)
            mb_server = Meteobridge(session, host, username, password, unit_system)

            await mb_server.update()

            return True
        except UnexpectedError:
            # The data retriever will raise an issue if something goes wrong
            pass

        return False

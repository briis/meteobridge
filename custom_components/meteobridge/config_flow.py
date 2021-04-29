"""Config flow to configure Meteobridge Integration."""
import logging

from pymeteobridgeio import (
    Meteobridge,
    InvalidCredentials,
    ResultError,
    SUPPORTED_LANGUAGES,
)

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_ID,
    CONF_HOST,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
)

from homeassistant.core import callback
from homeassistant.helpers import aiohttp_client

from .const import (
    DOMAIN,
    CONF_LANGUAGE,
    CONF_EXTRA_SENSORS,
    CONF_UNIT_TEMPERATURE,
    CONF_UNIT_WIND,
    CONF_UNIT_RAIN,
    CONF_UNIT_PRESSURE,
    CONF_UNIT_DISTANCE,
    DEFAULT_LANGUAGE,
    DEFAULT_SCAN_INTERVAL,
    WIND_UNITS,
    RAIN_UNITS,
    PRESSURE_UNITS,
    DISTANCE_UNITS,
    UNIT_TYPE_DIST_KM,
    UNIT_TYPE_DIST_MI,
    UNIT_TYPE_PRESSURE_HPA,
    UNIT_TYPE_PRESSURE_INHG,
    UNIT_TYPE_RAIN_MM,
    UNIT_TYPE_RAIN_IN,
    UNIT_TYPE_TEMP_CELCIUS,
    UNIT_TYPE_WIND_MS,
    UNIT_TYPE_WIND_MPH,
)

_LOGGER = logging.getLogger(__name__)


class MeteobridgeFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a Meteobridge config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

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
        mb_server = Meteobridge(
            user_input[CONF_HOST],
            user_input[CONF_USERNAME],
            user_input[CONF_PASSWORD],
            UNIT_TYPE_TEMP_CELCIUS,
            user_input[CONF_UNIT_WIND],
            user_input[CONF_UNIT_RAIN],
            user_input[CONF_UNIT_PRESSURE],
            user_input[CONF_UNIT_DISTANCE],
            DEFAULT_LANGUAGE,
            0,
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
                CONF_UNIT_TEMPERATURE: UNIT_TYPE_TEMP_CELCIUS,
                CONF_UNIT_WIND: user_input.get(CONF_UNIT_WIND),
                CONF_UNIT_RAIN: user_input.get(CONF_UNIT_RAIN),
                CONF_UNIT_PRESSURE: user_input.get(CONF_UNIT_PRESSURE),
                CONF_UNIT_DISTANCE: user_input.get(CONF_UNIT_DISTANCE),
                CONF_LANGUAGE: user_input.get(CONF_LANGUAGE),
                CONF_EXTRA_SENSORS: user_input.get(CONF_EXTRA_SENSORS),
                CONF_SCAN_INTERVAL: user_input.get(CONF_SCAN_INTERVAL),
            },
        )

    async def _show_setup_form(self, errors=None):
        """Show the setup form to the user."""

        if self.hass.config.units.is_metric:
            _unit_wind = UNIT_TYPE_WIND_MS
            _unit_rain = UNIT_TYPE_RAIN_MM
            _unit_pressure = UNIT_TYPE_PRESSURE_HPA
            _unit_distance = UNIT_TYPE_DIST_KM
        else:
            _unit_wind = UNIT_TYPE_WIND_MPH
            _unit_rain = UNIT_TYPE_RAIN_IN
            _unit_pressure = UNIT_TYPE_PRESSURE_INHG
            _unit_distance = UNIT_TYPE_DIST_MI

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_USERNAME, default="meteobridge"): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_UNIT_WIND, default=_unit_wind): vol.In(
                        WIND_UNITS
                    ),
                    vol.Required(CONF_UNIT_RAIN, default=_unit_rain): vol.In(
                        RAIN_UNITS
                    ),
                    vol.Required(CONF_UNIT_PRESSURE, default=_unit_pressure): vol.In(
                        PRESSURE_UNITS
                    ),
                    vol.Required(CONF_UNIT_DISTANCE, default=_unit_distance): vol.In(
                        DISTANCE_UNITS
                    ),
                    vol.Optional(CONF_LANGUAGE, default=DEFAULT_LANGUAGE): vol.In(
                        SUPPORTED_LANGUAGES
                    ),
                    vol.Optional(CONF_EXTRA_SENSORS, default=0): vol.All(
                        vol.Coerce(int), vol.Range(min=0, max=2)
                    ),
                    vol.Optional(
                        CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                    ): vol.All(vol.Coerce(int), vol.Range(min=5, max=60)),
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

        if self.hass.config.units.is_metric:
            _unit_wind = UNIT_TYPE_WIND_MS
            _unit_rain = UNIT_TYPE_RAIN_MM
            _unit_pressure = UNIT_TYPE_PRESSURE_HPA
            _unit_distance = UNIT_TYPE_DIST_KM
        else:
            _unit_wind = UNIT_TYPE_WIND_MPH
            _unit_rain = UNIT_TYPE_RAIN_IN
            _unit_pressure = UNIT_TYPE_PRESSURE_INHG
            _unit_distance = UNIT_TYPE_DIST_MI

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_UNIT_WIND,
                        default=self.config_entry.options.get(
                            CONF_UNIT_WIND, _unit_wind
                        ),
                    ): vol.In(WIND_UNITS),
                    vol.Required(
                        CONF_UNIT_RAIN,
                        default=self.config_entry.options.get(
                            CONF_UNIT_RAIN, _unit_rain
                        ),
                    ): vol.In(RAIN_UNITS),
                    vol.Required(
                        CONF_UNIT_PRESSURE,
                        default=self.config_entry.options.get(
                            CONF_UNIT_PRESSURE, _unit_pressure
                        ),
                    ): vol.In(PRESSURE_UNITS),
                    vol.Required(
                        CONF_UNIT_DISTANCE,
                        default=self.config_entry.options.get(
                            CONF_UNIT_DISTANCE, _unit_distance
                        ),
                    ): vol.In(DISTANCE_UNITS),
                    vol.Optional(
                        CONF_LANGUAGE,
                        default=self.config_entry.options.get(
                            CONF_LANGUAGE, DEFAULT_LANGUAGE
                        ),
                    ): vol.In(SUPPORTED_LANGUAGES),
                    vol.Optional(
                        CONF_EXTRA_SENSORS,
                        default=self.config_entry.options.get(CONF_EXTRA_SENSORS, 0),
                    ): vol.All(vol.Coerce(int), vol.Range(min=0, max=2)),
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=5, max=60)),
                }
            ),
        )

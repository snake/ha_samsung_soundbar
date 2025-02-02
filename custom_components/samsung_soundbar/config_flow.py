import logging

import pysmartthings
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from pysmartthings import APIResponseError

from .const import (CONF_ENTRY_API_KEY, CONF_ENTRY_DEVICE_ID,
                    CONF_ENTRY_DEVICE_NAME, CONF_ENTRY_MAX_VOLUME, DOMAIN)

_LOGGER = logging.getLogger(__name__)


async def validate_input(api, device_id: str):
    try:
        return await api.device(device_id)
    except APIResponseError as excp:
        _LOGGER.error("[Samsung Soundbar] ERROR: %s", str(excp))
        raise ValueError


class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        _LOGGER.error(f"Example Flow starts with user_input {user_input}")
        if user_input is not None:
            _LOGGER.error(f"User Input is not filled")
            try:
                session = async_get_clientsession(self.hass)
                api = pysmartthings.SmartThings(
                    session, user_input.get(CONF_ENTRY_API_KEY)
                )
                _LOGGER.error(f"Validating Input {user_input}")
                device = await validate_input(api, user_input.get(CONF_ENTRY_DEVICE_ID))

                _LOGGER.error(
                    f"Successfully validated Input, Creating entry with title {DOMAIN} and data {user_input}"
                )
                return self.async_create_entry(title=DOMAIN, data=user_input)
            except Exception as excp:
                _LOGGER.error(f"Example Flow triggered an exception {excp}")
                return self.async_abort(reason="fetch_failed")

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ENTRY_API_KEY): str,
                    vol.Required(CONF_ENTRY_DEVICE_ID): str,
                    vol.Required(CONF_ENTRY_DEVICE_NAME): str,
                    vol.Required(CONF_ENTRY_MAX_VOLUME): int,
                }
            ),
        )

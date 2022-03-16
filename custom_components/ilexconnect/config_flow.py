import voluptuous as vol
from homeassistant import config_entries

from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD
)

from .const import (
    DOMAIN
)

class ILexConnectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a I-LexConnect config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_USERNAME],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            )
        )

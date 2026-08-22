"""Config flow for Feel24 Visitors."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CENTERS,
    CENTERS_BY_ID,
    CONF_CENTER_NAME,
    CONF_LOCATION_ID,
    DOMAIN,
)

CENTER_SELECTOR = SelectSelector(
    SelectSelectorConfig(
        options=[
            SelectOptionDict(value=location_id, label=name)
            for location_id, name in CENTERS
        ],
        mode=SelectSelectorMode.DROPDOWN,
        custom_value=False,
    )
)


class Feel24VisitorsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Feel24 Visitors."""

    VERSION = 3

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle setup initiated by the user."""
        errors: dict[str, str] = {}

        if user_input is not None:
            location_id = str(user_input.get(CONF_LOCATION_ID, ""))
            center_name = CENTERS_BY_ID.get(location_id)

            if center_name is None:
                errors["base"] = "invalid_center"
            else:
                await self.async_set_unique_id(location_id)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=center_name,
                    data={
                        CONF_CENTER_NAME: center_name,
                        CONF_LOCATION_ID: location_id,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_LOCATION_ID): CENTER_SELECTOR}),
            errors=errors,
        )

"""Config flow for Feel24 Visitors."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_GYM,
    CONF_GYM_ID,
    DEFAULT_NAME,
    DOMAIN,
    DYNAMIC_UNIQUE_ID,
)
from .gyms import GYMS, get_gym, gym_unique_id, resolve_gym

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_GYM): SelectSelector(
            SelectSelectorConfig(
                options=list(GYMS),
                custom_value=True,
                mode=SelectSelectorMode.DROPDOWN,
                sort=True,
            )
        )
    }
)


class Feel24VisitorsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Feel24 Visitors."""

    VERSION = 2

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial configuration step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            gym = resolve_gym(user_input.get(CONF_GYM))

            if gym is None:
                errors[CONF_GYM] = "unknown_gym"
            else:
                gym_data = get_gym(gym)
                await self.async_set_unique_id(
                    gym_unique_id(gym_data) if gym_data else DYNAMIC_UNIQUE_ID
                )
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=gym or DEFAULT_NAME,
                    data={
                        CONF_GYM: gym,
                        CONF_GYM_ID: gym_data.id if gym_data else None,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                CONFIG_SCHEMA, user_input or {}
            ),
            errors=errors,
        )

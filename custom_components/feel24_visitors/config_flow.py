"""Config flow for Feel24 Visitors."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.const import Platform
from homeassistant.core import callback, split_entity_id
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TimeSelector,
)

from .const import (
    CENTERS,
    CENTERS_BY_ID,
    CONF_CENTER_NAME,
    CONF_LOCATION_ID,
    CONF_NOTIFICATION_END,
    CONF_NOTIFICATION_START,
    CONF_NOTIFICATION_TARGET,
    CONF_NOTIFICATION_THRESHOLD,
    CONF_NOTIFICATION_TIME_MODE,
    DEFAULT_NOTIFICATION_END,
    DEFAULT_NOTIFICATION_START,
    DEFAULT_NOTIFICATION_THRESHOLD,
    DOMAIN,
    NOTIFICATION_TIME_MODE_ALL_DAY,
    NOTIFICATION_TIME_MODE_WINDOW,
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

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> Feel24VisitorsOptionsFlow:
        """Create the options flow."""
        return Feel24VisitorsOptionsFlow()

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


class Feel24VisitorsOptionsFlow(OptionsFlow):
    """Configure visitor notifications."""

    def __init__(self) -> None:
        """Initialize the options flow."""
        self._pending_options: dict[str, Any] | None = None

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Configure threshold, schedule mode, and notification target."""
        errors: dict[str, str] = {}

        if user_input is not None:
            target = str(user_input[CONF_NOTIFICATION_TARGET])
            if not self._is_valid_notify_entity(target):
                errors[CONF_NOTIFICATION_TARGET] = "invalid_recipient"
            else:
                options = dict(self.config_entry.options)
                options.update(
                    {
                        CONF_NOTIFICATION_THRESHOLD: int(
                            user_input[CONF_NOTIFICATION_THRESHOLD]
                        ),
                        CONF_NOTIFICATION_TIME_MODE: user_input[
                            CONF_NOTIFICATION_TIME_MODE
                        ],
                        CONF_NOTIFICATION_TARGET: target,
                    }
                )

                if (
                    options[CONF_NOTIFICATION_TIME_MODE]
                    == NOTIFICATION_TIME_MODE_ALL_DAY
                ):
                    options.setdefault(
                        CONF_NOTIFICATION_START, DEFAULT_NOTIFICATION_START
                    )
                    options.setdefault(CONF_NOTIFICATION_END, DEFAULT_NOTIFICATION_END)
                    return self.async_create_entry(data=options)

                self._pending_options = options
                return await self.async_step_schedule()

        current = dict(self.config_entry.options)
        suggested_values: dict[str, Any] = {
            CONF_NOTIFICATION_THRESHOLD: current.get(
                CONF_NOTIFICATION_THRESHOLD, DEFAULT_NOTIFICATION_THRESHOLD
            ),
            CONF_NOTIFICATION_TIME_MODE: current.get(
                CONF_NOTIFICATION_TIME_MODE, NOTIFICATION_TIME_MODE_ALL_DAY
            ),
        }
        if target := current.get(CONF_NOTIFICATION_TARGET):
            suggested_values[CONF_NOTIFICATION_TARGET] = target
        if user_input is not None:
            suggested_values.update(user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_NOTIFICATION_THRESHOLD): vol.All(
                    NumberSelector(
                        NumberSelectorConfig(
                            min=0,
                            max=1000,
                            step=1,
                            mode=NumberSelectorMode.BOX,
                        )
                    ),
                    vol.Coerce(int),
                ),
                vol.Required(CONF_NOTIFICATION_TIME_MODE): SelectSelector(
                    SelectSelectorConfig(
                        options=[
                            SelectOptionDict(
                                value=NOTIFICATION_TIME_MODE_ALL_DAY,
                                label="Hele døgnet",
                            ),
                            SelectOptionDict(
                                value=NOTIFICATION_TIME_MODE_WINDOW,
                                label="Mellom to klokkeslett",
                            ),
                        ],
                        mode=SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Required(CONF_NOTIFICATION_TARGET): EntitySelector(
                    EntitySelectorConfig(domain=Platform.NOTIFY)
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                schema, suggested_values
            ),
            errors=errors,
        )

    async def async_step_schedule(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Configure a restricted notification time window."""
        errors: dict[str, str] = {}

        if user_input is not None:
            if (
                user_input[CONF_NOTIFICATION_START]
                == user_input[CONF_NOTIFICATION_END]
            ):
                errors["base"] = "same_notification_time"
            elif self._pending_options is not None:
                self._pending_options.update(user_input)
                return self.async_create_entry(data=self._pending_options)

        current = dict(self.config_entry.options)
        suggested_values = {
            CONF_NOTIFICATION_START: current.get(
                CONF_NOTIFICATION_START, DEFAULT_NOTIFICATION_START
            ),
            CONF_NOTIFICATION_END: current.get(
                CONF_NOTIFICATION_END, DEFAULT_NOTIFICATION_END
            ),
        }
        if user_input is not None:
            suggested_values.update(user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_NOTIFICATION_START): TimeSelector(),
                vol.Required(CONF_NOTIFICATION_END): TimeSelector(),
            }
        )
        return self.async_show_form(
            step_id="schedule",
            data_schema=self.add_suggested_values_to_schema(
                schema, suggested_values
            ),
            errors=errors,
        )

    def _is_valid_notify_entity(self, entity_id: str) -> bool:
        """Return whether the selected recipient is a registered notify entity."""
        entity_registry = er.async_get(self.hass)
        resolved_entity_id = er.async_resolve_entity_id(
            entity_registry, entity_id
        )
        if resolved_entity_id is None:
            return False
        if split_entity_id(resolved_entity_id)[0] != Platform.NOTIFY:
            return False

        return (
            self.hass.states.get(resolved_entity_id) is not None
            or entity_registry.async_get(resolved_entity_id) is not None
        )

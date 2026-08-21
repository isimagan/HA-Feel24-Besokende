"""Config flow for Feel24 Visitors."""

from __future__ import annotations

from collections.abc import Mapping
import re
from typing import Any

from aiohttp import ClientError
import voluptuous as vol

from homeassistant.config_entries import (
    SOURCE_REAUTH,
    ConfigFlow,
    ConfigFlowResult,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .api import (
    Feel24Api,
    Feel24ApiError,
    Feel24AuthChallenge,
    Feel24Credentials,
    Feel24InvalidCodeError,
    Feel24InvalidPhoneError,
    Feel24RateLimitError,
)
from .const import (
    CONF_ACCESS_TOKEN,
    CONF_CODE,
    CONF_GYM,
    CONF_GYM_ID,
    CONF_PHONE,
    CONF_USER_ID,
    DEFAULT_NAME,
    DOMAIN,
    DYNAMIC_UNIQUE_ID,
)
from .gyms import GYMS, get_gym, gym_unique_id, resolve_gym

GYM_SCHEMA = vol.Schema(
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

PHONE_SCHEMA = vol.Schema({vol.Required(CONF_PHONE): str})
CODE_SCHEMA = vol.Schema({vol.Required(CONF_CODE): str})


class Feel24VisitorsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Feel24 Visitors."""

    VERSION = 3

    def __init__(self) -> None:
        """Initialize flow-only login state."""
        self._pending_gym = ""
        self._pending_gym_id: int | None = None
        self._phone = ""
        self._challenge: Feel24AuthChallenge | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Choose the gym for a new config entry."""
        errors: dict[str, str] = {}

        if user_input is not None:
            gym = resolve_gym(user_input.get(CONF_GYM))

            if gym is None:
                errors[CONF_GYM] = "unknown_gym"
            else:
                gym_data = get_gym(gym)
                await self.async_set_unique_id(
                    gym_unique_id(gym_data)
                    if gym_data
                    else DYNAMIC_UNIQUE_ID
                )
                self._abort_if_unique_id_configured()

                self._pending_gym = gym
                self._pending_gym_id = gym_data.id if gym_data else None

                existing_credentials = self._existing_credentials()
                if existing_credentials is not None:
                    return self._create_entry(existing_credentials)
                return await self.async_step_phone()

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                GYM_SCHEMA, user_input or {}
            ),
            errors=errors,
        )

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Start reauthentication for a missing or expired member token."""
        self._phone = str(entry_data.get(CONF_PHONE, ""))
        return await self.async_step_phone()

    async def async_step_phone(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Request the member's phone number and send a login code."""
        errors: dict[str, str] = {}

        if user_input is not None:
            phone = _normalize_phone(str(user_input.get(CONF_PHONE, "")))
            if phone is None:
                errors[CONF_PHONE] = "invalid_phone"
            else:
                api = Feel24Api(async_get_clientsession(self.hass))
                try:
                    challenge = await api.async_start_authentication(phone)
                except Feel24InvalidPhoneError:
                    errors[CONF_PHONE] = "invalid_phone"
                except Feel24RateLimitError:
                    errors["base"] = "rate_limited"
                except (Feel24ApiError, ClientError, TimeoutError):
                    errors["base"] = "cannot_connect"
                else:
                    self._phone = phone
                    self._challenge = challenge
                    return await self.async_step_code()

        suggested_values = user_input or {CONF_PHONE: self._phone}
        return self.async_show_form(
            step_id="phone",
            data_schema=self.add_suggested_values_to_schema(
                PHONE_SCHEMA, suggested_values
            ),
            errors=errors,
        )

    async def async_step_code(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Verify the one-time code and finish authentication."""
        errors: dict[str, str] = {}

        if self._challenge is None:
            return await self.async_step_phone()

        if user_input is not None:
            code = str(user_input.get(CONF_CODE, "")).strip()
            if not code:
                errors[CONF_CODE] = "invalid_code"
            else:
                api = Feel24Api(async_get_clientsession(self.hass))
                try:
                    credentials = await api.async_complete_authentication(
                        self._challenge, code
                    )
                except Feel24InvalidCodeError:
                    errors[CONF_CODE] = "invalid_code"
                except Feel24RateLimitError:
                    errors["base"] = "rate_limited"
                except (Feel24ApiError, ClientError, TimeoutError):
                    errors["base"] = "cannot_connect"
                else:
                    return self._finish_authentication(credentials)

        return self.async_show_form(
            step_id="code",
            data_schema=CODE_SCHEMA,
            errors=errors,
            description_placeholders={"phone": self._phone},
        )

    def _existing_credentials(self) -> dict[str, str | int] | None:
        """Reuse the authenticated account when another gym is added."""
        for entry in self.hass.config_entries.async_entries(DOMAIN):
            token = entry.data.get(CONF_ACCESS_TOKEN)
            user_id = entry.data.get(CONF_USER_ID)
            phone = entry.data.get(CONF_PHONE)
            if (
                isinstance(token, str)
                and token
                and isinstance(user_id, int)
                and isinstance(phone, str)
            ):
                return {
                    CONF_ACCESS_TOKEN: token,
                    CONF_USER_ID: user_id,
                    CONF_PHONE: phone,
                }
        return None

    def _finish_authentication(
        self, credentials: Feel24Credentials
    ) -> ConfigFlowResult:
        """Create a new entry or update all gym entries after reauth."""
        credential_data: dict[str, str | int] = {
            CONF_ACCESS_TOKEN: credentials.token,
            CONF_USER_ID: credentials.user_id,
            CONF_PHONE: self._phone,
        }

        if self.source == SOURCE_REAUTH:
            reauth_entry = self._get_reauth_entry()
            for entry in self.hass.config_entries.async_entries(DOMAIN):
                if entry.entry_id == reauth_entry.entry_id:
                    continue
                self.hass.config_entries.async_update_entry(
                    entry,
                    data={**entry.data, **credential_data},
                )

            return self.async_update_reload_and_abort(
                reauth_entry,
                data_updates=credential_data,
            )

        return self._create_entry(credential_data)

    def _create_entry(
        self, credentials: Mapping[str, str | int]
    ) -> ConfigFlowResult:
        """Create a configured gym entry."""
        return self.async_create_entry(
            title=self._pending_gym or DEFAULT_NAME,
            data={
                CONF_GYM: self._pending_gym,
                CONF_GYM_ID: self._pending_gym_id,
                **credentials,
            },
        )


def _normalize_phone(value: str) -> str | None:
    """Normalize Norwegian and international phone numbers for iBooking."""
    phone = re.sub(r"[\s()-]", "", value)
    if phone.startswith("00"):
        phone = f"+{phone[2:]}"
    elif phone.isdigit() and len(phone) == 8:
        phone = f"+47{phone}"

    if not re.fullmatch(r"\+[1-9]\d{7,14}", phone):
        return None
    return phone

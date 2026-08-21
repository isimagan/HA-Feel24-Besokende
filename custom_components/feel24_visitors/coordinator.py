"""Data coordinator for Feel24 Visitors."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from aiohttp import ClientError
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import (
    Feel24Api,
    Feel24ApiError,
    Feel24AuthenticationError,
)
from .const import (
    CONF_ACCESS_TOKEN,
    CONF_GYM,
    CONF_GYM_ID,
    CONF_USER_ID,
    DEFAULT_NAME,
)
from .gyms import get_gym, select_effective_gym

UPDATE_INTERVAL = timedelta(minutes=5)


@dataclass(frozen=True, slots=True)
class Feel24VisitorsData:
    """Current Feel24 visitor data."""

    gym: str
    gym_id: int | None
    visitor_count: int | None


class Feel24VisitorsCoordinator(DataUpdateCoordinator[Feel24VisitorsData]):
    """Coordinate the selected gym and its visitor count."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self._fixed_gym = entry.data.get(CONF_GYM, "")
        self._chosen_gym = entry.options.get(CONF_GYM, "")
        self._api = Feel24Api(async_get_clientsession(hass))

        super().__init__(
            hass,
            logger=entry.logger,
            name=DEFAULT_NAME,
            update_interval=UPDATE_INTERVAL,
            config_entry=entry,
            always_update=False,
        )

    @property
    def gym(self) -> str:
        """Return the gym currently used by the visitor sensor."""
        return select_effective_gym(self._fixed_gym, self._chosen_gym)

    @property
    def has_fixed_gym(self) -> bool:
        """Return whether the gym was fixed in the config flow."""
        return bool(self._fixed_gym)

    @property
    def gym_id(self) -> int | None:
        """Return the iBooking ID for the active gym."""
        gym = get_gym(self.gym)
        return gym.id if gym else None

    async def _async_update_data(self) -> Feel24VisitorsData:
        """Fetch visitor data for the selected gym."""
        token = self.entry.data.get(CONF_ACCESS_TOKEN)
        user_id = self.entry.data.get(CONF_USER_ID)
        if not isinstance(token, str) or not isinstance(user_id, int):
            raise ConfigEntryAuthFailed("Feel24 login is required")

        visitor_count: int | None = None
        if self.gym_id is not None:
            try:
                visitor_count = await self._api.async_get_visitor_count(
                    self.gym_id, token, user_id
                )
            except Feel24AuthenticationError as err:
                raise ConfigEntryAuthFailed(
                    "Feel24 credentials were rejected"
                ) from err
            except (Feel24ApiError, ClientError, TimeoutError) as err:
                raise UpdateFailed(
                    "Error communicating with the Feel24 API"
                ) from err

        return Feel24VisitorsData(
            gym=self.gym,
            gym_id=self.gym_id,
            visitor_count=visitor_count,
        )

    async def async_set_gym(self, gym: str) -> None:
        """Persist a user-selected gym and refresh the visitor sensor."""
        gym_data = get_gym(gym)
        if gym_data is None:
            raise ValueError(f"Unknown Feel24 gym: {gym}")

        self._chosen_gym = gym_data.name
        self.hass.config_entries.async_update_entry(
            self.entry,
            options={
                **self.entry.options,
                CONF_GYM: gym_data.name,
                CONF_GYM_ID: gym_data.id,
            },
        )
        await self.async_refresh()

"""Data coordinator for Feel24 Visitors."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CONF_GYM, DEFAULT_NAME
from .gyms import select_effective_gym

UPDATE_INTERVAL = timedelta(minutes=5)


@dataclass(frozen=True, slots=True)
class Feel24VisitorsData:
    """Current Feel24 visitor data."""

    gym: str
    visitor_count: int | None


class Feel24VisitorsCoordinator(DataUpdateCoordinator[Feel24VisitorsData]):
    """Coordinate the selected gym and its visitor count."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self._fixed_gym = entry.data.get(CONF_GYM, "")
        self._chosen_gym = entry.options.get(CONF_GYM, "")

        super().__init__(
            hass,
            logger=entry.logger,
            name=DEFAULT_NAME,
            update_interval=UPDATE_INTERVAL,
            config_entry=entry,
        )

    @property
    def gym(self) -> str:
        """Return the gym currently used by the visitor sensor."""
        return select_effective_gym(self._fixed_gym, self._chosen_gym)

    @property
    def has_fixed_gym(self) -> bool:
        """Return whether the gym was fixed in the config flow."""
        return bool(self._fixed_gym)

    async def _async_update_data(self) -> Feel24VisitorsData:
        """Fetch visitor data for the selected gym.

        The app confirms that visitor statistics exist, but no anonymous public
        endpoint has been verified yet. Keep the value unknown instead of
        publishing an invented count.
        """
        return Feel24VisitorsData(gym=self.gym, visitor_count=None)

    async def async_set_gym(self, gym: str) -> None:
        """Persist a user-selected gym and refresh the visitor sensor."""
        self._chosen_gym = gym
        self.hass.config_entries.async_update_entry(
            self.entry,
            options={**self.entry.options, CONF_GYM: gym},
        )
        await self.async_refresh()

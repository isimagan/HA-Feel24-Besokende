"""Data update coordinator for Feel24 Visitors."""

from __future__ import annotations

import asyncio
import logging

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import BASE_VISITORS_URL, CONF_LOCATION_ID, DOMAIN, UPDATE_INTERVAL
from .parser import parse_visitor_count

_LOGGER = logging.getLogger(__name__)


class Feel24VisitorsCoordinator(DataUpdateCoordinator[int]):
    """Fetch the current visitor count for one Feel24 center."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.location_id = str(entry.data[CONF_LOCATION_ID])
        self.visitors_url = (
            f"{BASE_VISITORS_URL}?location={self.location_id}&page=visitors"
        )
        self._session = async_get_clientsession(hass)

        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=f"{DOMAIN}_{self.location_id}",
            update_interval=UPDATE_INTERVAL,
            always_update=False,
        )

    async def _async_update_data(self) -> int:
        """Fetch and parse the current visitor count."""
        try:
            async with asyncio.timeout(10):
                async with self._session.get(self.visitors_url) as response:
                    response.raise_for_status()
                    html = await response.text(encoding="iso-8859-1")

            return parse_visitor_count(html)
        except (TimeoutError, aiohttp.ClientError, UnicodeError, ValueError) as err:
            raise UpdateFailed(f"Kunne ikke hente besøkstallet fra Feel24: {err}") from err

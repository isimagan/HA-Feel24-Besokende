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

_MAX_RESPONSE_BYTES = 256 * 1024
_READ_CHUNK_BYTES = 16 * 1024


async def _read_bounded_response(response: aiohttp.ClientResponse) -> str:
    """Read a visitor page without allowing an unbounded response body."""
    if (
        response.content_length is not None
        and response.content_length > _MAX_RESPONSE_BYTES
    ):
        raise ValueError("Feel24 response is too large")

    body = bytearray()
    async for chunk in response.content.iter_chunked(_READ_CHUNK_BYTES):
        body.extend(chunk)
        if len(body) > _MAX_RESPONSE_BYTES:
            raise ValueError("Feel24 response is too large")

    return body.decode("iso-8859-1")


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
                    html = await _read_bounded_response(response)

            return parse_visitor_count(html)
        except (TimeoutError, aiohttp.ClientError, UnicodeError, ValueError) as err:
            raise UpdateFailed(f"Kunne ikke hente besøkstallet fra Feel24: {err}") from err

"""The Feel24 Visitors integration."""

from __future__ import annotations

from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import STATIC_URL_PATH
from .coordinator import Feel24VisitorsCoordinator

PLATFORMS = (Platform.SELECT, Platform.SENSOR)
STATIC_DIR = Path(__file__).parent / "static"


async def async_setup(hass: HomeAssistant, _config: ConfigType) -> bool:
    """Set up integration-wide resources."""
    await hass.http.async_register_static_paths(
        [StaticPathConfig(STATIC_URL_PATH, str(STATIC_DIR), True)]
    )
    return True


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry
) -> bool:
    """Set up Feel24 Visitors from a config entry."""
    coordinator = Feel24VisitorsCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: ConfigEntry
) -> bool:
    """Unload a Feel24 Visitors config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

"""Feel24 Visitors integration."""

from pathlib import Path
from typing import Any

from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    CENTERS_BY_ID,
    CONF_CENTER_NAME,
    CONF_LOCATION_ID,
    ENTITY_PICTURE_URL,
)
from .coordinator import Feel24VisitorsCoordinator

PLATFORMS = [Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up the Feel24 Visitors integration."""
    icon_path = Path(__file__).parent / "brand" / "icon.png"
    await hass.http.async_register_static_paths(
        [StaticPathConfig(ENTITY_PICTURE_URL, str(icon_path), True)]
    )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Feel24 Visitors from a config entry."""
    coordinator = Feel24VisitorsCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Feel24 Visitors config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate an older Feel24 Visitors config entry."""
    if entry.version == 1:
        location_id = str(entry.data[CONF_LOCATION_ID])
        center_name = CENTERS_BY_ID.get(location_id)
        if center_name is None:
            return False

        hass.config_entries.async_update_entry(
            entry,
            data={
                **entry.data,
                CONF_CENTER_NAME: center_name,
            },
            title=center_name,
            version=2,
        )

    return True

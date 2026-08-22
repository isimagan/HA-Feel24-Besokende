"""Feel24 Visitors integration."""

from pathlib import Path
from typing import Any

from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.util import slugify

from .const import (
    CENTERS_BY_ID,
    CONF_CENTER_NAME,
    CONF_LOCATION_ID,
    DOMAIN,
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
    if entry.version > 3:
        return False

    data = dict(entry.data)
    location_id = str(data[CONF_LOCATION_ID])
    center_name = data.get(CONF_CENTER_NAME)

    if entry.version == 1:
        center_name = CENTERS_BY_ID.get(location_id)
        if center_name is None:
            return False

        data[CONF_CENTER_NAME] = center_name

    if not isinstance(center_name, str):
        return False

    if entry.version <= 2:
        entity_registry = er.async_get(hass)
        old_unique_id = f"{location_id}_visitors"
        entity_id = entity_registry.async_get_entity_id(
            Platform.SENSOR, DOMAIN, old_unique_id
        )

        if entity_id is not None:
            old_default_entity_id = f"sensor.{slugify(f'{center_name} Visitors')}"
            new_entity_id = (
                f"sensor.{slugify(f'{center_name} Besøkende')}"
                if entity_id == old_default_entity_id
                else entity_id
            )
            entity_registry.async_update_entity(
                entity_id,
                new_entity_id=new_entity_id,
                new_unique_id=f"{location_id}_besokende",
            )

    hass.config_entries.async_update_entry(
        entry,
        data=data,
        title=center_name,
        version=3,
    )

    return True

"""The Feel24 Visitors integration."""

from __future__ import annotations

from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_GYM,
    CONF_GYM_ID,
    DOMAIN,
    DYNAMIC_UNIQUE_ID,
    STATIC_URL_PATH,
)
from .coordinator import Feel24VisitorsCoordinator
from .gyms import get_gym, gym_unique_id, resolve_gym

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
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


async def async_migrate_entry(
    hass: HomeAssistant, entry: ConfigEntry
) -> bool:
    """Migrate older entries to per-gym IDs and unique IDs."""
    if entry.version > 3:
        return False

    if entry.version == 1:
        fixed_gym_name = resolve_gym(entry.data.get(CONF_GYM))
        if fixed_gym_name is None:
            entry.logger.error(
                "Cannot migrate unknown Feel24 gym: %s",
                entry.data.get(CONF_GYM),
            )
            return False

        fixed_gym = get_gym(fixed_gym_name)
        chosen_gym = get_gym(entry.options.get(CONF_GYM))

        data = {
            **entry.data,
            CONF_GYM: fixed_gym_name,
            CONF_GYM_ID: fixed_gym.id if fixed_gym else None,
        }
        options = dict(entry.options)
        if chosen_gym:
            options.update(
                {CONF_GYM: chosen_gym.name, CONF_GYM_ID: chosen_gym.id}
            )

        hass.config_entries.async_update_entry(
            entry,
            data=data,
            options=options,
            title=fixed_gym_name or entry.title,
            unique_id=(
                gym_unique_id(fixed_gym)
                if fixed_gym
                else DYNAMIC_UNIQUE_ID
            ),
            version=3,
        )

    elif entry.version == 2:
        hass.config_entries.async_update_entry(entry, version=3)

    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: ConfigEntry
) -> bool:
    """Unload a Feel24 Visitors config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

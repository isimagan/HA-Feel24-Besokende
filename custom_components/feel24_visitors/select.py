"""Select platform for Feel24 Visitors."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CHOSEN_GYM_ICON
from .coordinator import Feel24VisitorsCoordinator
from .gyms import GYMS


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the optional gym selector."""
    coordinator: Feel24VisitorsCoordinator = entry.runtime_data
    if not coordinator.has_fixed_gym:
        async_add_entities([Feel24ChosenGymSelect(coordinator, entry.entry_id)])


class Feel24ChosenGymSelect(SelectEntity):
    """Select the gym used by the Feel24 visitor sensor."""

    _attr_name = "Feel24 Chosen Gym"
    _attr_icon = CHOSEN_GYM_ICON
    _attr_options = list(GYMS)

    def __init__(
        self, coordinator: Feel24VisitorsCoordinator, entry_id: str
    ) -> None:
        """Initialize the gym selector."""
        self.coordinator = coordinator
        self._attr_unique_id = f"{entry_id}_chosen_gym"

    @property
    def current_option(self) -> str | None:
        """Return the gym currently used by the visitor sensor."""
        return self.coordinator.gym or None

    async def async_select_option(self, option: str) -> None:
        """Change the gym used by the visitor sensor."""
        if option not in GYMS:
            raise ValueError(f"Unknown Feel24 gym: {option}")
        await self.coordinator.async_set_gym(option)
        self.async_write_ha_state()

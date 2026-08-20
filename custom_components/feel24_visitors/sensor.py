"""Sensor platform for Feel24 Visitors."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_GYM,
    ENTITY_PICTURE_URL,
    VISITORS_ICON,
    VISITORS_UNIT,
)
from .coordinator import Feel24VisitorsCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Feel24 visitor sensor."""
    async_add_entities([Feel24VisitorsSensor(entry.runtime_data, entry.entry_id)])


class Feel24VisitorsSensor(
    CoordinatorEntity[Feel24VisitorsCoordinator], SensorEntity
):
    """Show the current number of visitors at the selected Feel24 gym."""

    _attr_name = "Feel24 Visitors"
    _attr_entity_picture = ENTITY_PICTURE_URL
    _attr_icon = VISITORS_ICON
    _attr_native_unit_of_measurement = VISITORS_UNIT
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self, coordinator: Feel24VisitorsCoordinator, entry_id: str
    ) -> None:
        """Initialize the visitor sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_visitors"

    @property
    def available(self) -> bool:
        """Return whether a verified visitor count is available."""
        return (
            super().available
            and bool(self.coordinator.data.gym)
            and self.coordinator.data.visitor_count is not None
        )

    @property
    def native_value(self) -> int | None:
        """Return the current visitor count."""
        return self.coordinator.data.visitor_count

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return the gym represented by the visitor count."""
        return {ATTR_GYM: self.coordinator.data.gym}

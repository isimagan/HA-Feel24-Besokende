"""Sensor platform for Feel24 Visitors."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_CENTER_ID,
    BASE_VISITORS_URL,
    CONF_CENTER_NAME,
    CONF_LOCATION_ID,
    DOMAIN,
    ENTITY_PICTURE_URL,
    ICON,
)
from .coordinator import Feel24VisitorsCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Feel24 visitor sensor from a config entry."""
    async_add_entities([Feel24VisitorsSensor(entry, entry.runtime_data)])


class Feel24VisitorsSensor(
    CoordinatorEntity[Feel24VisitorsCoordinator], SensorEntity
):
    """Representation of the current visitor count at a Feel24 center."""

    _attr_has_entity_name = True
    _attr_icon = ICON
    _attr_name = "Visitors"
    _attr_native_unit_of_measurement = "besøkende"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self, entry: ConfigEntry, coordinator: Feel24VisitorsCoordinator
    ) -> None:
        """Initialize the visitor sensor."""
        super().__init__(coordinator)

        location_id = str(entry.data[CONF_LOCATION_ID])
        center_name = str(entry.data[CONF_CENTER_NAME])

        self._attr_unique_id = f"{location_id}_visitors"
        self._attr_entity_picture = ENTITY_PICTURE_URL
        self._attr_extra_state_attributes = {ATTR_CENTER_ID: location_id}
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, location_id)},
            name=center_name,
            manufacturer="Feel24",
            configuration_url=(
                f"{BASE_VISITORS_URL}?location={location_id}&page=visitors"
            ),
        )

    @property
    def native_value(self) -> int:
        """Return the current visitor count."""
        return self.coordinator.data

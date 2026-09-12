"""Sensor platform for Feel24 Visitors."""

from __future__ import annotations

import re

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import (
    ATTR_CENTER_ID,
    ATTR_CONFIG_ENTRY_ID,
    ATTR_CUSTOM_UI_MORE_INFO,
    ATTR_LOGO_PATH,
    ATTR_NOTIFICATION_SWITCH,
    ATTR_PLACE,
    BASE_VISITORS_URL,
    CONF_CENTER_NAME,
    CONF_LOCATION_ID,
    DOMAIN,
    ENTITY_PICTURE_URL,
    ICON,
    LOGO_PATH_URL,
    MORE_INFO_ELEMENT,
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
    _attr_name = "Besøkende"
    _attr_native_unit_of_measurement = "besøkende"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self, entry: ConfigEntry, coordinator: Feel24VisitorsCoordinator
    ) -> None:
        """Initialize the visitor sensor."""
        super().__init__(coordinator)

        location_id = str(entry.data[CONF_LOCATION_ID])
        center_name = str(entry.data[CONF_CENTER_NAME])

        place = re.sub(r"^Feel\s*24\s+", "", center_name, flags=re.IGNORECASE)

        self._location_id = location_id
        self._default_notification_switch_entity_id = (
            f"switch.{slugify(f'{center_name} Varsel')}"
        )
        self._attr_unique_id = f"{location_id}_besokende"
        self._attr_entity_picture = ENTITY_PICTURE_URL
        self._attr_extra_state_attributes = {
            ATTR_CENTER_ID: location_id,
            ATTR_CONFIG_ENTRY_ID: entry.entry_id,
            ATTR_CUSTOM_UI_MORE_INFO: MORE_INFO_ELEMENT,
            ATTR_LOGO_PATH: LOGO_PATH_URL,
            ATTR_NOTIFICATION_SWITCH: self._default_notification_switch_entity_id,
            ATTR_PLACE: place,
        }
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, location_id)},
            name=center_name,
            manufacturer="Feel24",
            configuration_url=(
                f"{BASE_VISITORS_URL}?location={location_id}&page=visitors"
            ),
        )

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return frontend metadata with the current notification switch ID."""
        attributes = dict(self._attr_extra_state_attributes)
        entity_registry = er.async_get(self.hass)
        switch_entity_id = entity_registry.async_get_entity_id(
            Platform.SWITCH, DOMAIN, f"{self._location_id}_varsel"
        )
        if switch_entity_id is not None:
            attributes[ATTR_NOTIFICATION_SWITCH] = switch_entity_id
        return attributes

    @property
    def native_value(self) -> int:
        """Return the current visitor count."""
        return self.coordinator.data

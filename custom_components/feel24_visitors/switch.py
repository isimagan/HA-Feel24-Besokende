"""Switch platform for Feel24 visitor notifications."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.notify.const import (
    ATTR_MESSAGE,
    ATTR_TITLE,
    DOMAIN as NOTIFY_DOMAIN,
    SERVICE_SEND_MESSAGE,
)
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, STATE_ON
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import (
    BASE_VISITORS_URL,
    CONF_CENTER_NAME,
    CONF_LOCATION_ID,
    CONF_NOTIFICATION_END,
    CONF_NOTIFICATION_START,
    CONF_NOTIFICATION_TARGET,
    CONF_NOTIFICATION_THRESHOLD,
    CONF_NOTIFICATION_TIME_MODE,
    DEFAULT_NOTIFICATION_END,
    DEFAULT_NOTIFICATION_START,
    DEFAULT_NOTIFICATION_THRESHOLD,
    DOMAIN,
    NOTIFICATION_ICON_OFF,
    NOTIFICATION_ICON_ON,
    NOTIFICATION_TIME_MODE_ALL_DAY,
)
from .coordinator import Feel24VisitorsCoordinator
from .notification import (
    crossed_threshold,
    is_within_time_window,
    notification_message,
    numeric_visitor_count,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Feel24 visitor notification switch."""
    async_add_entities([Feel24VisitorNotificationSwitch(entry, entry.runtime_data)])


class Feel24VisitorNotificationSwitch(
    CoordinatorEntity[Feel24VisitorsCoordinator], RestoreEntity, SwitchEntity
):
    """Enable or disable threshold notifications for a Feel24 center."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True
    _attr_name = "Varsel"
    _attr_should_poll = False

    def __init__(
        self, entry: ConfigEntry, coordinator: Feel24VisitorsCoordinator
    ) -> None:
        """Initialize the notification switch."""
        super().__init__(coordinator)

        self._entry = entry
        self._location_id = str(entry.data[CONF_LOCATION_ID])
        self._center_name = str(entry.data[CONF_CENTER_NAME])
        self._attr_unique_id = f"{self._location_id}_varsel"
        self._attr_is_on = False
        self._previous_count: int | float | None = None
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._location_id)},
            name=self._center_name,
            manufacturer="Feel24",
            configuration_url=(
                f"{BASE_VISITORS_URL}?location={self._location_id}&page=visitors"
            ),
        )

    async def async_added_to_hass(self) -> None:
        """Restore the user's switch choice and establish a count baseline."""
        await super().async_added_to_hass()

        if (last_state := await self.async_get_last_state()) is not None:
            self._attr_is_on = last_state.state == STATE_ON
        else:
            self._attr_is_on = False

        if self.coordinator.last_update_success:
            self._previous_count = numeric_visitor_count(self.coordinator.data)

    @property
    def icon(self) -> str:
        """Return an icon matching the switch state."""
        return NOTIFICATION_ICON_ON if self.is_on else NOTIFICATION_ICON_OFF

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Enable visitor notifications."""
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Disable visitor notifications."""
        self._attr_is_on = False
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Evaluate a new visitor count without starting another poll."""
        if not self.coordinator.last_update_success:
            super()._handle_coordinator_update()
            return

        current = numeric_visitor_count(self.coordinator.data)
        if current is None:
            super()._handle_coordinator_update()
            return

        previous = self._previous_count
        self._previous_count = current

        if self.is_on and self._should_notify(previous, current):
            self.hass.async_create_task(
                self._async_send_notification(current),
                f"Feel24 visitor notification for {self._center_name}",
            )

        super()._handle_coordinator_update()

    def _should_notify(
        self,
        previous: int | float | None,
        current: int | float,
    ) -> bool:
        """Return whether all notification requirements are met."""
        options = self._entry.options
        target = options.get(CONF_NOTIFICATION_TARGET)
        if not isinstance(target, str) or self._resolve_target(target) is None:
            return False

        threshold = numeric_visitor_count(
            options.get(
                CONF_NOTIFICATION_THRESHOLD, DEFAULT_NOTIFICATION_THRESHOLD
            )
        )
        if threshold is None or not crossed_threshold(previous, current, threshold):
            return False

        if (
            options.get(
                CONF_NOTIFICATION_TIME_MODE, NOTIFICATION_TIME_MODE_ALL_DAY
            )
            == NOTIFICATION_TIME_MODE_ALL_DAY
        ):
            return True

        return is_within_time_window(
            dt_util.now().time(),
            str(options.get(CONF_NOTIFICATION_START, DEFAULT_NOTIFICATION_START)),
            str(options.get(CONF_NOTIFICATION_END, DEFAULT_NOTIFICATION_END)),
        )

    async def _async_send_notification(self, count: int | float) -> None:
        """Send the threshold notification to the configured notify entity."""
        target = self._entry.options.get(CONF_NOTIFICATION_TARGET)
        if not isinstance(target, str) or (
            resolved_target := self._resolve_target(target)
        ) is None:
            return

        try:
            await self.hass.services.async_call(
                NOTIFY_DOMAIN,
                SERVICE_SEND_MESSAGE,
                {
                    ATTR_TITLE: self._center_name,
                    ATTR_MESSAGE: notification_message(count, self._center_name),
                },
                blocking=True,
                target={"entity_id": resolved_target},
            )
        except HomeAssistantError as err:
            _LOGGER.warning(
                "Kunne ikke sende Feel24-varsel til %s: %s", resolved_target, err
            )

    def _resolve_target(self, entity_id_or_uuid: str) -> str | None:
        """Resolve the selected notify entity and reject removed recipients."""
        entity_registry = er.async_get(self.hass)
        entity_id = er.async_resolve_entity_id(entity_registry, entity_id_or_uuid)
        if entity_id is None or not entity_id.startswith(f"{NOTIFY_DOMAIN}."):
            return None
        return entity_id if self.hass.states.get(entity_id) is not None else None

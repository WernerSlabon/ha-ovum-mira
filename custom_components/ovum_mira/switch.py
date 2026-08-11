"""Switch platform for Ovum Mira integration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL, REG_WW_SWITCH, SLAVE_HSM
from .coordinator import OvumMiraCoordinator


@dataclass
class OvumMiraSwitchEntityDescription(SwitchEntityDescription):
    """Describes Ovum Mira switch entity."""

    value_fn: Callable[[dict[str, Any]], Any] | None = None
    register: int | None = None
    slave: int = SLAVE_HSM


# Placeholder for potential switches (e.g., enable/disable features)
# Add specific switches based on your device's capabilities
SWITCH_TYPES: tuple[OvumMiraSwitchEntityDescription, ...] = (
    # Example:
    # OvumMiraSwitchEntityDescription(
    #     key="enable_pv_mode",
    #     name="PV Modus aktivieren",
    #     value_fn=lambda data: data.get("pv_mode_enabled", False),
    #     register=55100,  # Replace with actual register
    # ),
    OvumMiraSwitchEntityDescription(
        key="ww_switch",
        name="WW Hauptschalter",
        has_entity_name=True,
        value_fn=lambda data: data.get("ww_switch", False),
        register=REG_WW_SWITCH,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ovum Mira switch based on a config entry."""
    coordinator: OvumMiraCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(OvumMiraSwitch(coordinator, description, entry) for description in SWITCH_TYPES)


class OvumMiraSwitch(CoordinatorEntity[OvumMiraCoordinator], SwitchEntity):
    """Representation of an Ovum Mira switch."""

    entity_description: OvumMiraSwitchEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: OvumMiraCoordinator,
        description: OvumMiraSwitchEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Ovum Mira",
            "manufacturer": MANUFACTURER,
            "model": MODEL,
        }

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        if self.entity_description.value_fn:
            return bool(self.entity_description.value_fn(self.coordinator.data))
        return False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        if self.entity_description.register:
            await self.coordinator.async_write_register(
                self.entity_description.register,
                1,
                self.entity_description.slave,
            )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        if self.entity_description.register:
            await self.coordinator.async_write_register(
                self.entity_description.register,
                0,
                self.entity_description.slave,
            )

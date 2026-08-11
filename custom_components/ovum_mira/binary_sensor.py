"""Binary Sensor platform for Ovum Mira integration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL
from .coordinator import OvumMiraCoordinator


@dataclass
class OvumMiraBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes Ovum Mira binary sensor entity."""

    value_fn: Callable[[dict[str, Any]], Any] | None = None


BINARY_SENSOR_TYPES: tuple[OvumMiraBinarySensorEntityDescription, ...] = (
    OvumMiraBinarySensorEntityDescription(
        key="ww_system",
        name="WW installiert",
        value_fn=lambda data: data.get("ww_system"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ovum Mira sensor based on a config entry."""
    coordinator: OvumMiraCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(OvumMiraBinarySensor(coordinator, description, entry) for description in BINARY_SENSOR_TYPES)


class OvumMiraBinarySensor(CoordinatorEntity[OvumMiraCoordinator], BinarySensorEntity):
    """Representation of an Ovum Mira sensor."""

    entity_description: OvumMiraBinarySensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: OvumMiraCoordinator,
        description: OvumMiraBinarySensorEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Ovum Mira",
            "manufacturer": MANUFACTURER,
            "model": MODEL,
            "sw_version": coordinator.data.get("software_version"),
        }

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on/active."""
        if self.entity_description.value_fn:
            return self.entity_description.value_fn(self.coordinator.data) != "0"
        return None

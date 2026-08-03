"""Select platform for Ovum Mira integration."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
		DOMAIN,
		MANUFACTURER,
		MODEL,
		REG_HK1_TYP,
		REG_HK1_MODE,
		REG_HK2_TYP,
		REG_HK2_MODE,
		REG_SYS_PUFFER,
		REG_EMS_PV_STATUS,
		SLAVE_HSM,
		SLAVE_WPM1,
)
from .coordinator import OvumMiraCoordinator


@dataclass
class OvumMiraSelectEntityDescription(SelectEntityDescription):
		"""Describes Ovum Mira select entity."""

		value_fn: Callable[[dict[str, Any]], Any] | None = None
		register: int | None = None
		slave: int = SLAVE_WPM1
		value_map: dict[str, int] | None = None

PUFFER_TYP = {
        'Nicht installiert' : 0,
        'Puffer' : 1,
        'Cubespeicher' : 2
}

PV_STATUS = {
	    'neutral' : 0,
        'increase' : 1,
        'reduce' : 2,
}

HK_TYP = {
        'Nicht installiert' : 0,
        'Ungeregelt' : 1,
        'Rücklauf' : 2,
        'Gemischt' : 3,
        'Cube Direkt' : 4,
}

HK_MODES = {
		"Aus": 0,
		"Automatik": 1,
		"Winter": 2,
		"Sommer": 3,
}

SELECT_TYPES: tuple[OvumMiraSelectEntityDescription, ...] = (
		OvumMiraSelectEntityDescription(
				key="sys_puffer",
				name="Puffer Typ",
				options=list(PUFFER_TYP.keys()),
				value_fn=lambda data: next(
						(k for k, v in PUFFER_TYP.items() if v == data.get("sys_puffer")),
						"Nicht installiert",
				),
				register=REG_SYS_PUFFER,
				value_map=PUFFER_TYP,
				slave=SLAVE_HSM,
		),
		OvumMiraSelectEntityDescription(
				key="ems_pv_status",
				name="EMS PV Status",
				translation_key="ems_pv_status",
				options=list(PV_STATUS.keys()),
				value_fn=lambda data: next(
						(k for k, v in PV_STATUS.items() if v == data.get("ems_pv_status")),
						"neutral",
				),
				register=REG_EMS_PV_STATUS,
				value_map=PV_STATUS,
				slave=SLAVE_HSM,
		),
		OvumMiraSelectEntityDescription(
				key="hk1_typ",
				name="HK1 Typ",
				options=list(HK_TYP.keys()),
				value_fn=lambda data: next(
						(k for k, v in HK_TYP.items() if v == data.get("hk1_typ")),
						"Nicht installiert",
				),
				register=REG_HK1_TYP,
				value_map=HK_TYP,
				slave=SLAVE_HSM,
		),
		OvumMiraSelectEntityDescription(
				key="hk1_mode",
				name="HK1 Betriebsart",
				options=list(HK_MODES.keys()),
				value_fn=lambda data: next(
						(k for k, v in HK_MODES.items() if v == data.get("hk1_mode")),
						"Automatik",
				),
				register=REG_HK1_MODE,
				value_map=HK_MODES,
				slave=SLAVE_HSM,
		),
		OvumMiraSelectEntityDescription(
				key="hk2_typ",
				name="HK2 Typ",
				options=list(HK_TYP.keys()),
				value_fn=lambda data: next(
						(k for k, v in HK_TYP.items() if v == data.get("hk2_typ")),
						"Nicht installiert",
				),
				register=REG_HK2_TYP,
				value_map=HK_TYP,
				slave=SLAVE_HSM,
		),
		OvumMiraSelectEntityDescription(
				key="hk2_mode",
				name="HK2 Betriebsart",
				options=list(HK_MODES.keys()),
				value_fn=lambda data: next(
						(k for k, v in HK_MODES.items() if v == data.get("hk2_mode")),
						"Automatik",
				),
				register=REG_HK2_MODE,
				value_map=HK_MODES,
				slave=SLAVE_HSM,
		),
)


async def async_setup_entry(
		hass: HomeAssistant,
		entry: ConfigEntry,
		async_add_entities: AddEntitiesCallback,
) -> None:
		"""Set up Ovum Mira select based on a config entry."""
		coordinator: OvumMiraCoordinator = hass.data[DOMAIN][entry.entry_id]

		async_add_entities(
				OvumMiraSelect(coordinator, description, entry)
				for description in SELECT_TYPES
		)


class OvumMiraSelect(CoordinatorEntity[OvumMiraCoordinator], SelectEntity):
		"""Representation of an Ovum Mira select entity."""

		entity_description: OvumMiraSelectEntityDescription
		_attr_has_entity_name = True

		def __init__(
				self,
				coordinator: OvumMiraCoordinator,
				description: OvumMiraSelectEntityDescription,
				entry: ConfigEntry,
		) -> None:
				"""Initialize the select entity."""
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
		def current_option(self) -> str | None:
				"""Return the current option."""
				if self.entity_description.value_fn:
						return self.entity_description.value_fn(self.coordinator.data)
				return None

		async def async_select_option(self, option: str) -> None:
				"""Change the selected option."""
				if (self.entity_description.register
					and self.entity_description.value_map
					and option in self.entity_description.value_map):
						
						value = self.entity_description.value_map[option]
						await self.coordinator.async_write_register(
							self.entity_description.register,
							value,
							self.entity_description.slave,
						)

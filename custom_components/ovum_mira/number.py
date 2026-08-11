"""Number platform for Ovum Mira integration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.number import NumberDeviceClass, NumberEntity, NumberEntityDescription, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfPower, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    MANUFACTURER,
    MODEL,
    REG_EMS_BATTERIE_SOC,
    REG_EMS_NETZ_POWER,
    REG_EMS_SOLL_POWER,
    REG_EMS_WR_POWER,
    REG_HK1_RAUM_SOLL,
    REG_HK2_RAUM_SOLL,
    REG_PUFFER_SOLL_PV,
    REG_WW_SOLL,
    REG_WW_SOLL_PV,
    SLAVE_HSM,
)
from .coordinator import OvumMiraCoordinator


@dataclass
class OvumMiraNumberEntityDescription(NumberEntityDescription):
    """Describes Ovum Mira number entity."""

    value_fn: Callable[[dict[str, Any]], Any] | None = None
    register: int | None = None
    register_type: str | None = None
    slave: int = SLAVE_HSM


NUMBER_TYPES: tuple[OvumMiraNumberEntityDescription, ...] = (
    # Warmwasser
    OvumMiraNumberEntityDescription(
        key="ww_soll",
        name="WW Soll",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        mode=NumberMode.BOX,
        native_min_value=10,
        native_max_value=65,
        native_step=1,
        value_fn=lambda data: data.get("ww_soll"),
        register=REG_WW_SOLL,
    ),
    OvumMiraNumberEntityDescription(
        key="ww_soll_pv",
        name="WW Soll (PV)",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        mode=NumberMode.BOX,
        native_min_value=10,
        native_max_value=65,
        native_step=1,
        value_fn=lambda data: data.get("ww_soll_pv"),
        register=REG_WW_SOLL_PV,
    ),
    # Heizpuffer
    OvumMiraNumberEntityDescription(
        key="puffer_soll_pv",
        name="Puffer Soll (PV)",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        mode=NumberMode.BOX,
        native_min_value=10,
        native_max_value=65,
        native_step=1,
        value_fn=lambda data: data.get("puffer_soll_pv"),
        register=REG_PUFFER_SOLL_PV,
    ),
    # Heizkreis 1
    OvumMiraNumberEntityDescription(
        key="hk1_raum_soll",
        name="HK1 Raumtemperatur Soll",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=10,
        native_max_value=30,
        native_step=0.5,
        value_fn=lambda data: data.get("hk1_raum_soll"),
        register=REG_HK1_RAUM_SOLL,
    ),
    # Heizkreis 2
    OvumMiraNumberEntityDescription(
        key="hk2_raum_soll",
        name="HK2 Raumtemperatur Soll",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=10,
        native_max_value=30,
        native_step=0.5,
        value_fn=lambda data: data.get("hk2_raum_soll"),
        register=REG_HK2_RAUM_SOLL,
    ),
    # EMS
    OvumMiraNumberEntityDescription(
        key="ems_batterie_soc",
        name="EMS Batterie SoC",
        device_class=NumberDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        mode=NumberMode.BOX,
        native_min_value=0,
        native_max_value=100,
        value_fn=lambda data: data.get("ems_batterie_soc"),
        register=REG_EMS_BATTERIE_SOC,
    ),
    OvumMiraNumberEntityDescription(
        key="ems_netz_power",
        name="EMS Netzbezug",
        device_class=NumberDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        mode=NumberMode.BOX,
        native_min_value=-100000,
        native_max_value=100000,
        value_fn=lambda data: data.get("ems_netz_power"),
        register=REG_EMS_NETZ_POWER,
        register_type="int32",
    ),
    OvumMiraNumberEntityDescription(
        key="ems_wr_power",
        name="EMS Wechselrichter",
        device_class=NumberDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        mode=NumberMode.BOX,
        native_min_value=-100000,
        native_max_value=100000,
        value_fn=lambda data: data.get("ems_wr_power"),
        register=REG_EMS_WR_POWER,
        register_type="int32",
    ),
    OvumMiraNumberEntityDescription(
        key="ems_soll_power",
        name="EMS Leistung Soll",
        device_class=NumberDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        mode=NumberMode.BOX,
        native_min_value=-100000,
        native_max_value=100000,
        value_fn=lambda data: data.get("ems_soll_power"),
        register=REG_EMS_SOLL_POWER,
        register_type="int32",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ovum Mira number based on a config entry."""
    coordinator: OvumMiraCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(OvumMiraNumber(coordinator, description, entry) for description in NUMBER_TYPES)


class OvumMiraNumber(CoordinatorEntity[OvumMiraCoordinator], NumberEntity):
    """Representation of an Ovum Mira number entity."""

    entity_description: OvumMiraNumberEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: OvumMiraCoordinator,
        description: OvumMiraNumberEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the number entity."""
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
    def native_value(self) -> float | None:
        """Return the current value."""
        if self.entity_description.value_fn:
            return self.entity_description.value_fn(self.coordinator.data)
        return None

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        if self.entity_description.register:
            if self.entity_description.register_type == "int32":
                await self.coordinator.async_write_register_int32(
                    self.entity_description.register,
                    int(value),
                    self.entity_description.slave,
                )
            else:
                await self.coordinator.async_write_register(
                    self.entity_description.register,
                    int(value),
                    self.entity_description.slave,
                )

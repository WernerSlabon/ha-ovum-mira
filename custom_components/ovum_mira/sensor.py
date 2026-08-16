"""Sensor platform for Ovum Mira integration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower, UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL
from .coordinator import OvumMiraCoordinator


@dataclass
class OvumMiraSensorEntityDescription(SensorEntityDescription):
    """Describes Ovum Mira sensor entity."""

    value_fn: Callable[[dict[str, Any]], Any] | None = None


SENSOR_TYPES: tuple[OvumMiraSensorEntityDescription, ...] = (
    # Warmwasser
    OvumMiraSensorEntityDescription(
        key="ww_desired_temp",
        name="WW Solltemperatur aktiv",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.get("ww_desired_temp"),
    ),
    OvumMiraSensorEntityDescription(
        key="ww_temp_oben",
        name="WW Speichertemperatur Oben",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.get("ww_temp_oben"),
    ),
    OvumMiraSensorEntityDescription(
        key="ww_temp_unten",
        name="WW Speichertemperatur Unten",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.get("ww_temp_unten"),
    ),
    # Heizpuffer
    OvumMiraSensorEntityDescription(
        key="puffer_soll_temp",
        name="Puffer Solltemperatur aktiv",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.get("puffer_soll_temp"),
    ),
    OvumMiraSensorEntityDescription(
        key="puffer_temp_oben",
        name="Puffer Temperatur Oben",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.get("puffer_temp_oben"),
    ),
    OvumMiraSensorEntityDescription(
        key="puffer_temp_unten",
        name="Puffer Temperatur Unten",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.get("puffer_temp_unten"),
    ),
    # Heizkreis 1
    OvumMiraSensorEntityDescription(
        key="hk1_pv_plus",
        name="HK1 PV Plus",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.KELVIN,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("hk1_pv_plus"),
    ),
    OvumMiraSensorEntityDescription(
        key="hk1_pv_minus",
        name="HK1 PV Minus",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.KELVIN,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("hk1_pv_minus"),
    ),
    OvumMiraSensorEntityDescription(
        key="hk1_vorlauf_soll",
        name="HK1 Vorlauf Soll",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.get("hk1_vorlauf_soll"),
    ),
    OvumMiraSensorEntityDescription(
        key="hk1_vorlauf_ist",
        name="HK1 Vorlauf Ist",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.get("hk1_vorlauf_ist"),
    ),
    OvumMiraSensorEntityDescription(
        key="hk1_raum_soll",
        name="HK1 Raumtemperatur Soll",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("hk1_raum_soll"),
    ),
    OvumMiraSensorEntityDescription(
        key="hk1_raum_ist",
        name="HK1 Raumtemperatur",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.get("hk1_raum_ist"),
    ),
    # Heizkreis 2
    OvumMiraSensorEntityDescription(
        key="hk2_pv_plus",
        name="HK2 PV Plus",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.KELVIN,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("hk2_pv_plus"),
    ),
    OvumMiraSensorEntityDescription(
        key="hk2_pv_minus",
        name="HK2 PV Minus",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.KELVIN,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("hk2_pv_minus"),
    ),
    OvumMiraSensorEntityDescription(
        key="hk2_vorlauf_soll",
        name="HK2 Vorlauf Soll",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.get("hk2_vorlauf_soll"),
    ),
    OvumMiraSensorEntityDescription(
        key="hk2_vorlauf_ist",
        name="HK2 Vorlauf Ist",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.get("hk2_vorlauf_ist"),
    ),
    OvumMiraSensorEntityDescription(
        key="hk2_raum_soll",
        name="HK2 Raumtemperatur Soll",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("hk2_raum_soll"),
    ),
    OvumMiraSensorEntityDescription(
        key="hk2_raum_ist",
        name="HK2 Raumtemperatur",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.get("hk2_raum_ist"),
    ),
    # Wärmepumpe WPM1
    OvumMiraSensorEntityDescription(
        key="wpm1_systype",
        name="WP Kurzbezeichnung",
        value_fn=lambda data: data.get("wpm1_systype"),
    ),
    OvumMiraSensorEntityDescription(
        key="wpm1_anfsoll",
        name="WP Anforderung",
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("wpm1_anfsoll"),
    ),
    OvumMiraSensorEntityDescription(
        key="wpm1_wp_pwr",
        name="WP Wärmepumpenleistung",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("wpm1_wp_pwr"),
    ),
    OvumMiraSensorEntityDescription(
        key="wpm1_ko_pwr",
        name="WP Kondensator Leistung",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("wpm1_ko_pwr"),
    ),
    OvumMiraSensorEntityDescription(
        key="wpm1_status",
        name="WP Status",
        device_class=SensorDeviceClass.ENUM,
        translation_key="wpm_status",
        options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        value_fn=lambda data: data.get("wpm1_status"),
    ),
    OvumMiraSensorEntityDescription(
        key="wpm1_koet",
        name="WP Kondensator Einlass",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.get("wpm1_koet"),
    ),
    OvumMiraSensorEntityDescription(
        key="wpm1_koat",
        name="WP Kondensator Auslass",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.get("wpm1_koat"),
    ),
    OvumMiraSensorEntityDescription(
        key="wpm1_betriebszeit",
        name="WP Betriebszeit",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("wpm1_betriebszeit"),
    ),
    OvumMiraSensorEntityDescription(
        key="hsm_aussentemp",
        name="Außentemperatur",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda data: data.get("hsm_aussentemp"),
    ),
    # System Info
    OvumMiraSensorEntityDescription(
        key="software_version",
        name="Softwareversion",
        value_fn=lambda data: data.get("software_version"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ovum Mira sensor based on a config entry."""
    coordinator: OvumMiraCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(OvumMiraSensor(coordinator, description, entry) for description in SENSOR_TYPES)


class OvumMiraSensor(CoordinatorEntity[OvumMiraCoordinator], SensorEntity):
    """Representation of an Ovum Mira sensor."""

    entity_description: OvumMiraSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: OvumMiraCoordinator,
        description: OvumMiraSensorEntityDescription,
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
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if self.entity_description.value_fn:
            return self.entity_description.value_fn(self.coordinator.data)
        return None

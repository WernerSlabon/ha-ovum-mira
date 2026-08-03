"""Data coordinator for Ovum Mira integration."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
		DOMAIN,
		REG_EMS_BATTERIE_SOC,
		REG_EMS_NETZ_POWER,
		REG_EMS_PV_STATUS,
		REG_EMS_SOLL_POWER,
		REG_EMS_WR_POWER,
		REG_HSM_AUSSENTEMP,
		REG_HK1_TYP,
		REG_HK1_PV_PLUS,
		REG_HK1_PV_MINUS,
		REG_HK1_VORLAUF_SOLL,
		REG_HK1_VORLAUF_IST,
		REG_HK1_MODE,
		REG_HK1_RAUM_SOLL,
		REG_HK1_RAUM_IST,
		REG_HK2_TYP,
		REG_HK2_PV_PLUS,
		REG_HK2_PV_MINUS,
		REG_HK2_VORLAUF_SOLL,
		REG_HK2_VORLAUF_IST,
		REG_HK2_MODE,
		REG_HK2_RAUM_SOLL,
		REG_HK2_RAUM_IST,
		REG_PUFFER_SOLL_PV,
		REG_PUFFER_SOLL_TEMP,
		REG_PUFFER_TEMP_OBEN,
		REG_PUFFER_TEMP_UNTEN,
		REG_SOFTWARE_VERSION,
		REG_SYS_PUFFER,
		REG_WPM1_SYSTYPE,
		REG_WPM1_ANFSOLL,
		REG_WPM1_WP_PWR,
		REG_WPM1_KO_PWR,
		REG_WPM1_STATUS,
		REG_WPM1_KOET,
		REG_WPM1_KOAT,
		REG_WPM1_RUNTIME,
		REG_WW_DESIRED_TEMP,
		REG_WW_SWITCH,
		REG_WW_SOLL,
		REG_WW_SOLL_PV,
		REG_WW_SYSTEM,
		REG_WW_TEMP_OBEN,
		REG_WW_TEMP_UNTEN,
		SCAN_INTERVAL_NORMAL,
		SLAVE_HSM,
		SLAVE_WPM1,
)
from .modbus_client import OvumMiraModbusClient

_LOGGER = logging.getLogger(__name__)


class OvumMiraCoordinator(DataUpdateCoordinator[dict[str, Any]]):
		"""Coordinator to manage data updates from Ovum Mira."""

		def __init__(self, hass: HomeAssistant, host: str, port: int) -> None:
				"""Initialize the coordinator."""
				super().__init__(
						hass,
						_LOGGER,
						name=DOMAIN,
						update_interval=timedelta(seconds=SCAN_INTERVAL_NORMAL),
				)
				self.host = host
				self.port = port
				self._client = OvumMiraModbusClient(host, port)
				self._connected = False

		async def _async_update_data(self) -> dict[str, Any]:
				"""Fetch data from Ovum Mira."""
				try:
						if not self._connected:
								if not await self.hass.async_add_executor_job(self._client.connect):
										raise UpdateFailed("Failed to connect to Ovum Mira")
								self._connected = True

						data: dict[str, Any] = {}

						# Read all sensor values
						data.update(await self._read_warmwasser())
						data.update(await self._read_heizpuffer())
						data.update(await self._read_ems())
						data.update(await self._read_heizkreis1())
						data.update(await self._read_heizkreis2())
						data.update(await self._read_waermepumpe())
						data.update(await self._read_system_info())

						return data

				except Exception as err:
						self._connected = False
						raise UpdateFailed(f"Error communicating with device: {err}") from err

		async def _read_warmwasser(self) -> dict[str, Any]:
				"""Read warmwasser (hot water) data."""
				return {
						"ww_switch": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_WW_SWITCH, SLAVE_HSM
						),			
						"ww_soll": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_WW_SOLL, SLAVE_HSM
						),
						"ww_soll_pv": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_WW_SOLL_PV, SLAVE_HSM
						),
						"ww_desired_temp": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_WW_DESIRED_TEMP, SLAVE_HSM
						),
						"ww_system": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_WW_SYSTEM, SLAVE_HSM
						),
						"ww_temp_oben": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_WW_TEMP_OBEN, SLAVE_HSM
						),
						"ww_temp_unten": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_WW_TEMP_UNTEN, SLAVE_HSM
						),
				}

		async def _read_heizpuffer(self) -> dict[str, Any]:
				"""Read heating buffer data."""
				return {
						"sys_puffer": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_SYS_PUFFER, SLAVE_HSM
						),
						"puffer_soll_pv": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_PUFFER_SOLL_PV, SLAVE_HSM
						),
						"puffer_soll_temp": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_PUFFER_SOLL_TEMP, SLAVE_HSM
						),
						"puffer_temp_oben": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_PUFFER_TEMP_OBEN, SLAVE_HSM
						),
						"puffer_temp_unten": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_PUFFER_TEMP_UNTEN, SLAVE_HSM
						),
				}

		async def _read_ems(self) -> dict[str, Any]:
				"""Read energy management system data."""
				return {
						"ems_pv_status": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_EMS_PV_STATUS, SLAVE_HSM
						),
						"ems_batterie_soc": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_EMS_BATTERIE_SOC, SLAVE_HSM
						),
						"ems_netz_power": await self.hass.async_add_executor_job(
								self._client.read_int32, REG_EMS_NETZ_POWER, SLAVE_HSM
						),
						"ems_wr_power": await self.hass.async_add_executor_job(
								self._client.read_int32, REG_EMS_WR_POWER, SLAVE_HSM
						),
						"ems_soll_power": await self.hass.async_add_executor_job(
								self._client.read_int32, REG_EMS_SOLL_POWER, SLAVE_HSM
						),
				}

		async def _read_heizkreis1(self) -> dict[str, Any]:
				"""Read heating circuit 1 data."""
				return {
						"hk1_typ": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_HK1_TYP, SLAVE_HSM
						),
						"hk1_pv_plus": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_HK1_PV_PLUS, SLAVE_HSM
						),
						"hk1_pv_minus": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_HK1_PV_MINUS, SLAVE_HSM
						),
						"hk1_vorlauf_soll": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_HK1_VORLAUF_SOLL, SLAVE_HSM
						),
						"hk1_vorlauf_ist": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_HK1_VORLAUF_IST, SLAVE_HSM
						),
						"hk1_mode": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_HK1_MODE, SLAVE_HSM
						),				
						"hk1_raum_soll": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_HK1_RAUM_SOLL, SLAVE_HSM
						),				
						"hk1_raum_ist": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_HK1_RAUM_IST, SLAVE_HSM
						)				
				}

		async def _read_heizkreis2(self) -> dict[str, Any]:
				"""Read heating circuit 2 data."""
				return {
						"hk2_typ": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_HK2_TYP, SLAVE_HSM
						),
						"hk2_pv_plus": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_HK2_PV_PLUS, SLAVE_HSM
						),
						"hk2_pv_minus": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_HK2_PV_MINUS, SLAVE_HSM
						),
						"hk2_vorlauf_soll": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_HK2_VORLAUF_SOLL, SLAVE_HSM
						),
						"hk2_vorlauf_ist": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_HK2_VORLAUF_IST, SLAVE_HSM
						),
						"hk2_mode": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_HK2_MODE, SLAVE_HSM
						),				
						"hk2_raum_soll": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_HK2_RAUM_SOLL, SLAVE_HSM
						),				
						"hk2_raum_ist": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_HK2_RAUM_IST, SLAVE_HSM
						)				
				}

		async def _read_waermepumpe(self) -> dict[str, Any]:
				"""Read heat pump WPM1 data."""
				return {
						"wpm1_systype": await self.hass.async_add_executor_job(
								self._client.read_string, REG_WPM1_SYSTYPE, 10, SLAVE_WPM1
						),
						"wpm1_anfsoll": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_WPM1_ANFSOLL, SLAVE_WPM1
						),
						"wpm1_wp_pwr": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_WPM1_WP_PWR, SLAVE_WPM1
						),
						"wpm1_ko_pwr": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_WPM1_KO_PWR, SLAVE_WPM1
						),
						"wpm1_status": await self.hass.async_add_executor_job(
								self._client.read_int16, REG_WPM1_STATUS, SLAVE_WPM1
						),
						"wpm1_koet": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_WPM1_KOET, SLAVE_WPM1
						),
						"wpm1_koat": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_WPM1_KOAT, SLAVE_WPM1
						),
						"wpm1_betriebszeit": await self.hass.async_add_executor_job(
								self._client.read_int32, REG_WPM1_RUNTIME, SLAVE_WPM1
						),
				}

		async def _read_system_info(self) -> dict[str, Any]:
				"""Read system information."""
				return {
						"software_version": await self.hass.async_add_executor_job(
								self._client.read_string, REG_SOFTWARE_VERSION, 8, SLAVE_HSM
						),
						"hsm_aussentemp": await self.hass.async_add_executor_job(
								self._client.read_float32, REG_HSM_AUSSENTEMP, SLAVE_HSM
						),
				}

		async def async_write_register(
				self, address: int, value: int, slave: int = SLAVE_HSM
		) -> bool:
				"""Write a value to a register."""
				try:
						result = await self.hass.async_add_executor_job(
								self._client.write_int16, address, value, slave
						)
						if result:
								# Refresh data after write
								await self.async_request_refresh()
						return result
				except Exception as err:
						_LOGGER.error("Error writing register %s: %s", address, err)
						return False

		async def async_write_register_int32(
				self, address: int, value: int, slave: int = SLAVE_HSM
		) -> bool:
				"""Write a value to a register."""
				try:
						result = await self.hass.async_add_executor_job(
								self._client.write_int32, address, value, slave
						)
						if result:
								# Refresh data after write
								await self.async_request_refresh()
						return result
				except Exception as err:
						_LOGGER.error("Error writing register %s: %s", address, err)
						return False

		async def async_shutdown(self) -> None:
				"""Shutdown the coordinator."""
				await self.hass.async_add_executor_job(self._client.close)
				self._connected = False

"""The Ovum Mira integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .coordinator import OvumMiraCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
		Platform.SENSOR,
		Platform.NUMBER,
		Platform.SELECT,
		Platform.SWITCH,
		Platform.BINARY_SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
		"""Set up Ovum Mira from a config entry."""
		_LOGGER.debug("Setting up Ovum Mira integration")

		coordinator = OvumMiraCoordinator(
				hass,
				entry.data[CONF_HOST],
				entry.data.get(CONF_PORT, 502),
		)

		await coordinator.async_config_entry_first_refresh()

		if not coordinator.last_update_success:
				raise ConfigEntryNotReady("Unable to connect to Ovum Mira")

		hass.data.setdefault(DOMAIN, {})
		hass.data[DOMAIN][entry.entry_id] = coordinator

		await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

		return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
		"""Unload a config entry."""
		if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
				coordinator = hass.data[DOMAIN].pop(entry.entry_id)
				await coordinator.async_shutdown()

		return unload_ok

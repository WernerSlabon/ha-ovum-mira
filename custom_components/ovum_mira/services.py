"""Services for Ovum Mira integration."""
from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN
from .coordinator import OvumMiraCoordinator

_LOGGER = logging.getLogger(__name__)

SERVICE_WRITE_REGISTER = "write_register"
SERVICE_WRITE_REGISTER_SCHEMA = vol.Schema(
		{
				vol.Required("address"): cv.positive_int,
				vol.Required("value"): cv.positive_int,
				vol.Optional("slave", default=110): cv.positive_int,
		}
)


async def async_setup_services(hass: HomeAssistant) -> None:
		"""Set up services for Ovum Mira integration."""

		async def handle_write_register(call: ServiceCall) -> None:
				"""Handle the write_register service call."""
				address = call.data["address"]
				value = call.data["value"]
				slave = call.data["slave"]

				# Get the first coordinator (assumes single device)
				coordinators = hass.data.get(DOMAIN, {})
				if not coordinators:
						_LOGGER.error("No Ovum Mira devices configured")
						return

				coordinator: OvumMiraCoordinator = next(iter(coordinators.values()))

				success = await coordinator.async_write_register(address, value, slave)
				if success:
						_LOGGER.info(
								"Successfully wrote value %s to register %s (slave %s)",
								value,
								address,
								slave,
						)
				else:
						_LOGGER.error(
								"Failed to write value %s to register %s (slave %s)",
								value,
								address,
								slave,
						)

		hass.services.async_register(
				DOMAIN,
				SERVICE_WRITE_REGISTER,
				handle_write_register,
				schema=SERVICE_WRITE_REGISTER_SCHEMA,
		)


async def async_unload_services(hass: HomeAssistant) -> None:
		"""Unload Ovum Mira services."""
		hass.services.async_remove(DOMAIN, SERVICE_WRITE_REGISTER)

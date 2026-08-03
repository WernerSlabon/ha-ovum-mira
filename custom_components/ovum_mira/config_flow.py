"""Config flow for Ovum Mira integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import CONF_LOGIN_CODE, DEFAULT_PORT, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
		{
				vol.Required(CONF_HOST): str,
				vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
				vol.Optional(CONF_LOGIN_CODE): int,
		}
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
		"""Validate the user input allows us to connect."""
		# Import here to avoid issues if pymodbus is not yet installed
		try:
				from .modbus_client import OvumMiraModbusClient
		except ImportError as err:
				_LOGGER.error("Failed to import modbus_client: %s", err)
				raise CannotConnect from err

		client = OvumMiraModbusClient(
				data[CONF_HOST],
				data.get(CONF_PORT, DEFAULT_PORT),
		)

		try:
				# Test connection
				if not await hass.async_add_executor_job(client.connect):
						raise CannotConnect

				# Login if code is provided
				if CONF_LOGIN_CODE in data and data[CONF_LOGIN_CODE]:
						if not await hass.async_add_executor_job(
								client.login, data[CONF_LOGIN_CODE]
						):
								raise InvalidAuth

				# Try to read software version
				version = await hass.async_add_executor_job(client.read_software_version)
				if version is None:
						raise CannotConnect

				await hass.async_add_executor_job(client.close)

				return {"title": f"Ovum Mira ({data[CONF_HOST]})", "version": version}

		except Exception as err:
				_LOGGER.exception("Unexpected exception during validation")
				raise CannotConnect from err
		finally:
				await hass.async_add_executor_job(client.close)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
		"""Handle a config flow for Ovum Mira."""

		VERSION = 1

		async def async_step_user(
				self, user_input: dict[str, Any] | None = None
		) -> FlowResult:
				"""Handle the initial step."""
				errors: dict[str, str] = {}

				if user_input is not None:
						try:
								info = await validate_input(self.hass, user_input)
						except CannotConnect:
								errors["base"] = "cannot_connect"
						except InvalidAuth:
								errors["base"] = "invalid_auth"
						except Exception:  # pylint: disable=broad-except
								_LOGGER.exception("Unexpected exception")
								errors["base"] = "unknown"
						else:
								await self.async_set_unique_id(user_input[CONF_HOST])
								self._abort_if_unique_id_configured()

								return self.async_create_entry(title=info["title"], data=user_input)

				return self.async_show_form(
						step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
				)


class CannotConnect(HomeAssistantError):
		"""Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
		"""Error to indicate there is invalid auth."""

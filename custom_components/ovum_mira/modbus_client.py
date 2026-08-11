"""Modbus client for Ovum Mira heat pump."""

from __future__ import annotations

import logging
import struct

from pymodbus.client import ModbusTcpClient

from .const import DEFAULT_TIMEOUT, REG_LOGIN, REG_SOFTWARE_VERSION, SLAVE_HSM

_LOGGER = logging.getLogger(__name__)


def registers_to_bytes(registers: list[int]) -> bytes:
    """Convert list of 16-bit registers to bytes (big endian)."""
    return b"".join(struct.pack(">H", reg) for reg in registers)


class OvumMiraModbusClient:
    """Modbus TCP client for Ovum Mira."""

    def __init__(self, host: str, port: int = 502) -> None:
        """Initialize the Modbus client."""
        self.host = host
        self.port = port
        self._client = ModbusTcpClient(
            host=host,
            port=port,
            timeout=DEFAULT_TIMEOUT,
        )
        self._logged_in = False

    def connect(self) -> bool:
        """Connect to the Modbus device."""
        try:
            if not self._client.connect():
                _LOGGER.error("Failed to connect to %s:%s", self.host, self.port)
                return False
            _LOGGER.debug("Connected to %s:%s", self.host, self.port)
            return True
        except Exception as err:
            _LOGGER.error("Error connecting to %s:%s: %s", self.host, self.port, err)
            return False

    def close(self) -> None:
        """Close the Modbus connection."""
        try:
            self._client.close()
            _LOGGER.debug("Closed connection to %s:%s", self.host, self.port)
        except Exception as err:
            _LOGGER.error("Error closing connection: %s", err)

    def login(self, login_code: int) -> bool:
        """Send login code to the device."""
        try:
            # Convert login code to 32-bit big endian
            payload = struct.pack(">I", login_code)
            # Split into two 16-bit registers
            reg1 = struct.unpack(">H", payload[0:2])[0]
            reg2 = struct.unpack(">H", payload[2:4])[0]

            result = self._client.write_registers(
                REG_LOGIN,
                [reg1, reg2],
                device_id=SLAVE_HSM,
            )

            if result.isError():
                _LOGGER.error("Failed to send login code")
                return False

            self._logged_in = True
            _LOGGER.debug("Successfully sent login code")
            return True

        except Exception as err:
            _LOGGER.error("Error sending login code: %s", err)
            return False

    def read_software_version(self) -> str | None:
        """Read software version from device."""
        try:
            result = self._client.read_holding_registers(
                REG_SOFTWARE_VERSION,
                count=8,
                device_id=SLAVE_HSM,
            )

            if result.isError():
                _LOGGER.error("Failed to read software version")
                return None

            # Convert registers to string
            data = registers_to_bytes(result.registers)
            version = data.decode("ascii", errors="ignore").strip("\x00")
            _LOGGER.debug("Software version: %s", version)
            return version

        except Exception as err:
            _LOGGER.error("Error reading software version: %s", err)
            return None

    def read_int16(self, address: int, device_id: int = SLAVE_HSM) -> int | None:
        """Read a 16-bit signed integer."""
        try:
            result = self._client.read_holding_registers(address, count=1, device_id=device_id)
            if result.isError():
                return None

            # Convert register to signed int16
            value = result.registers[0]
            if value >= 32768:
                value -= 65536
            return value

        except Exception as err:
            _LOGGER.error("Error reading int16 at %s: %s", address, err)
            return None

    def read_uint16(self, address: int, device_id: int = SLAVE_HSM) -> int | None:
        """Read a 16-bit unsigned integer."""
        try:
            result = self._client.read_holding_registers(address, count=1, device_id=device_id)
            if result.isError():
                return None

            return result.registers[0]

        except Exception as err:
            _LOGGER.error("Error reading uint16 at %s: %s", address, err)
            return None

    def read_int32(self, address: int, device_id: int = SLAVE_HSM) -> int | None:
        """Read a 32-bit signed integer."""
        try:
            result = self._client.read_holding_registers(address, count=2, device_id=device_id)
            if result.isError():
                return None

            # Convert two registers to int32 (big endian)
            data = registers_to_bytes(result.registers)
            value = struct.unpack(">i", data)[0]
            return value

        except Exception as err:
            _LOGGER.error("Error reading int32 at %s: %s", address, err)
            return None

    def read_float32(self, address: int, device_id: int = SLAVE_HSM) -> float | None:
        """Read a 32-bit float."""
        try:
            result = self._client.read_holding_registers(address, count=2, device_id=device_id)
            if result.isError():
                return None

            # Convert two registers to float32 (big endian)
            data = registers_to_bytes(result.registers)
            value = struct.unpack(">f", data)[0]
            return value

        except Exception as err:
            _LOGGER.error("Error reading float32 at %s: %s", address, err)
            return None

    def write_int16(self, address: int, value: int, device_id: int = SLAVE_HSM) -> bool:
        """Write a 16-bit signed integer."""
        try:
            # Convert signed int to unsigned for Modbus
            if value < 0:
                value = (1 << 16) + value

            result = self._client.write_register(address, value, device_id=device_id)
            return not result.isError()

        except Exception as err:
            _LOGGER.error("Error writing int16 at %s: %s", address, err)
            return False

    def write_int32(self, address: int, value: int, device_id: int = SLAVE_HSM) -> bool:
        """Write a 32-bit signed integer."""
        try:
            # Convert to bytes and split into registers
            payload = struct.pack(">i", value)
            reg1 = struct.unpack(">H", payload[0:2])[0]
            reg2 = struct.unpack(">H", payload[2:4])[0]

            result = self._client.write_registers(address, [reg1, reg2], device_id=device_id)
            return not result.isError()

        except Exception as err:
            _LOGGER.error("Error writing int32 at %s: %s", address, err)
            return False

    def read_string(self, address: int, count: int, device_id: int = SLAVE_HSM) -> str | None:
        """Read a string (ASCII)."""
        try:
            result = self._client.read_holding_registers(address, count=count, device_id=device_id)
            if result.isError():
                return None

            # Convert registers to string
            data = registers_to_bytes(result.registers)
            string = data.decode("ascii", errors="ignore").strip("\x00")
            return string

        except Exception as err:
            _LOGGER.error("Error reading string at %s: %s", address, err)
            return None

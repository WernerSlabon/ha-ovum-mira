# Ovum Mira Home Assistant Integration - AI Coding Instructions

## Project Overview
This is a **Home Assistant custom component** for integrating the Ovum Mira heat pump system via **Modbus TCP**. The integration provides read/write access to heat pump parameters across multiple subsystems: hot water (Warmwasser), heating buffer (Heizpuffer), heating circuits (Heizkreise 1-2), energy management (EMS), and heat pump modules (WPM1-8).

## Architecture

### Component Structure (Home Assistant Conventions)
- `__init__.py` - Entry point: defines `PLATFORMS`, manages coordinator lifecycle via `async_setup_entry`/`async_unload_entry`
- `config_flow.py` - ConfigFlow UI for adding devices: validates Modbus connection, handles optional login code
- `coordinator.py` - **Central data hub**: `OvumMiraCoordinator` polls all Modbus registers every 30s, exposes unified dict to entities
- `modbus_client.py` - Low-level Modbus abstraction: handles connection, login, typed reads/writes (int16, int32, float32)
- Platform files (`sensor.py`, `number.py`, `select.py`, `switch.py`) - Entity definitions using dataclass descriptors
- `services.py` - Custom service `ovum_mira.write_register` for advanced manual register writes

### Data Flow
1. **Coordinator polling** → `_async_update_data()` calls 7 helper methods (`_read_warmwasser()`, `_read_ems()`, etc.)
2. Each helper uses `hass.async_add_executor_job(self._client.read_*)` to run sync Modbus calls in executor
3. Aggregated data stored in `coordinator.data` dict with flat keys like `"ww_temp_oben"`, `"ems_netz_power"`
4. Entities use `value_fn` lambdas to extract their specific values from the shared dict
5. **Writes** (from number/select entities) go through `coordinator.async_write_register()` → `modbus_client.write_int16()`

### Modbus Protocol Specifics
- **Slave IDs**: `SLAVE_HSM = 110` (main controller), `SLAVE_WPM1-8 = 111-118` (heat pump modules)
- **Register addresses**: Defined in `const.py` with semantic names (e.g., `REG_WW_SOLL = 55001`)
- **Data types**: 
  - INT16: temperatures (°C as integers), mode values, status codes
  - FLOAT32: precise temperatures (2 registers, big-endian), COP values
  - INT32: power values (Watts, 2 registers)
- **Login**: Optional 32-bit code written to `REG_LOGIN = 101` (split into two 16-bit registers, big-endian)

## Development Patterns

### Adding New Entities
1. **Add register constant** to `const.py` (e.g., `REG_NEW_SENSOR: Final = 55999`)
2. **Update coordinator** method to read the value in appropriate helper (e.g., `_read_warmwasser()`)
3. **Add entity descriptor** to platform file's tuple (e.g., `SENSOR_TYPES` in `sensor.py`):
   ```python
   OvumMiraSensorEntityDescription(
       key="unique_key",  # Becomes entity_id suffix
       name="Display Name",
       device_class=SensorDeviceClass.TEMPERATURE,
       value_fn=lambda data: data.get("unique_key"),  # Must match coordinator dict key
   )
   ```
4. For writable entities (number/select): include `register=REG_NEW_SENSOR, slave=SLAVE_HSM`

### Modbus Read/Write Methods
- `read_int16(address, slave)` - Returns `int` or `None`
- `read_float32(address, slave)` - Returns `float` or `None` (reads 2 consecutive registers)
- `read_int32(address, slave)` - Returns signed `int` (reads 2 consecutive registers)
- `write_int16(address, value, slave)` - Returns `bool` (handles signed→unsigned conversion)
- All calls are **synchronous** - wrap in `hass.async_add_executor_job()` from async context

### Entity Naming Convention
- **German names** in entity descriptors (matches device UI): "WW" (Warmwasser), "HK1/HK2" (Heizkreis 1/2), "Puffer", "WPM1" (Wärmepumpenmodul 1)
- Keys use snake_case: `ww_temp_oben`, `hk1_vorlauf_ist`, `ems_netz_power`
- Translations in `translations/en.json` and `translations/de.json`

### Error Handling
- Config flow: Raises `CannotConnect` or `InvalidAuth` → displayed to user via `strings.json`
- Coordinator: `raise UpdateFailed(...)` on any read error → sets `coordinator.last_update_success = False`
- Modbus client: Returns `None`/`False` on errors, logs via `_LOGGER.error()`
- Connection auto-recovery: Coordinator sets `self._connected = False` on errors, reconnects on next poll

## Testing & Debugging

### Local Development
This is typically deployed to a **Home Assistant instance** at `\\ha-4\config\custom_components\ovum_mira`. 

### Testing Connection
```python
# In config_flow.py, validate_input() tests:
1. client.connect() - TCP connection
2. client.login(code) if provided - Modbus write to REG_LOGIN
3. client.read_software_version() - Modbus read from REG_SOFTWARE_VERSION
```

### Debug Logging
Enable in Home Assistant `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.ovum_mira: debug
    pymodbus: debug
```

### Manual Register Testing
Use service `ovum_mira.write_register` to test writes without entity restart:
```yaml
service: ovum_mira.write_register
data:
  address: 55001  # Register address
  value: 50       # Integer value
  slave: 110      # Default HSM
```

## Key Constraints

- **pymodbus 3.13.1** required (specified in `manifest.json` requirements)
- **No background polling** - relies on Home Assistant's `DataUpdateCoordinator` pattern (30s default via `SCAN_INTERVAL_NORMAL`)
- **Single device per entry** - Multi-device support would need per-coordinator device_info updates
- **No diagnostic entities yet** - Connection status, error counts not exposed (logged only)
- **Float precision**: Use `suggested_display_precision=1` for float temperatures in sensor descriptors

## Common Mistakes to Avoid

❌ **Don't** call async Modbus methods from coordinator (they're sync) - always wrap in `async_add_executor_job`
❌ **Don't** forget slave ID parameter - defaults to SLAVE_HSM, but WPM modules need SLAVE_WPM1-8
❌ **Don't** read float32/int32 with single-register methods - they require 2 consecutive registers
❌ **Don't** use negative values in write_int16 without signed→unsigned conversion (handled in modbus_client)
❌ **Don't** modify `coordinator.data` directly - it's replaced wholesale on each update

## File References

- Modbus register map: [const.py](../const.py) (lines 28-89)
- Data aggregation logic: [coordinator.py](../coordinator.py#L77-L98)
- Modbus protocol implementation: [modbus_client.py](../modbus_client.py)
- Entity descriptor pattern example: [sensor.py](../sensor.py#L36-L88)

"""Constants for the Ovum Mira integration."""
from typing import Final

DOMAIN: Final = "ovum_mira"

# Configuration
CONF_LOGIN_CODE: Final = "login_code"

# Device info
MANUFACTURER: Final = "Ovum"
MODEL: Final = "Mira"

# Modbus configuration
DEFAULT_PORT: Final = 502
DEFAULT_TIMEOUT: Final = 5
DEFAULT_DELAY: Final = 1

# Slave IDs
SLAVE_HSM: Final = 110  # Hauptsteuermodul
SLAVE_WPM1: Final = 111  # Wärmepumpenmodul 1
SLAVE_WPM2: Final = 112  # Wärmepumpenmodul 2
SLAVE_WPM3: Final = 113
SLAVE_WPM4: Final = 114
SLAVE_WPM5: Final = 115
SLAVE_WPM6: Final = 116
SLAVE_WPM7: Final = 117
SLAVE_WPM8: Final = 118

# Scan intervals (in seconds)
SCAN_INTERVAL_FAST: Final = 10  # For power values
SCAN_INTERVAL_NORMAL: Final = 30  # For temperature and status
SCAN_INTERVAL_SLOW: Final = 3600  # For static values

# Register addresses OK
REG_LOGIN: Final = 101
REG_SOFTWARE_VERSION: Final = 20
REG_HSM_AUSSENTEMP: Final = 56048

# Warmwasser (WW) OK
REG_WW_SWITCH: Final = 55000 ## NEU
REG_WW_SOLL: Final = 55001
REG_WW_SOLL_PV: Final = 55002
REG_WW_SYSTEM: Final = 55003   ## NEU
REG_WW_DESIRED_TEMP: Final = 55004
REG_WW_TEMP_OBEN: Final = 55007
REG_WW_TEMP_UNTEN: Final = 55009

# Heizpuffer OK
REG_SYS_PUFFER: Final = 55020
REG_PUFFER_SOLL_PV: Final = 55021
REG_PUFFER_SOLL_TEMP: Final = 55023
REG_PUFFER_TEMP_OBEN: Final = 55026
REG_PUFFER_TEMP_UNTEN: Final = 55028

# EMS (Energie Management) OK
REG_EMS_PV_STATUS: Final = 55070
REG_EMS_BATTERIE_SOC: Final = 55071
REG_EMS_NETZ_POWER: Final = 55072
REG_EMS_WR_POWER: Final = 55074
REG_EMS_SOLL_POWER: Final = 55076

# Heizkreis 1
REG_HK1_TYP: Final = 56050
REG_HK1_PV_PLUS: Final = 56051
REG_HK1_PV_MINUS: Final = 56052
REG_HK1_VORLAUF_SOLL: Final = 56053
REG_HK1_VORLAUF_IST: Final = 56055
REG_HK1_MODE: Final = 56057
REG_HK1_RAUM_SOLL: Final = 56058
REG_HK1_RAUM_IST: Final = 56152

# Heizkreis 2
REG_HK2_TYP: Final = 56060
REG_HK2_PV_PLUS: Final = 56061
REG_HK2_PV_MINUS: Final = 56062
REG_HK2_VORLAUF_SOLL: Final = 56063
REG_HK2_VORLAUF_IST: Final = 56065
REG_HK2_MODE: Final = 56067
REG_HK2_RAUM_SOLL: Final = 56068
REG_HK2_RAUM_IST: Final = 56162

# Wärmepumpe WPM1
REG_WPM1_SYSTYPE: Final = 56000
REG_WPM1_ANFSOLL: Final = 56020
REG_WPM1_WP_PWR: Final = 56021
REG_WPM1_KO_PWR: Final = 56023
REG_WPM1_STATUS: Final = 56025
REG_WPM1_KOET: Final = 56026
REG_WPM1_KOAT: Final = 56028
REG_WPM1_RUNTIME: Final = 56030

import logging
from datetime import timedelta

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.const import PERCENTAGE

DOMAIN = "ilexconnect"

UPDATE_INTERVAL = timedelta(minutes=5)
API_TIMEOUT = 20

LOGGER = logging.getLogger(__package__)

API_CS1    = "getCS1"            # water reserve percent
API_IWH    = "getIWH"            # inkomende waterhardheid (fH graden)
API_OWH    = "getOWH"            # uitgaande waterhardheid (fH graden)
API_SD1    = "getSD1"            # zout reserve in dagen
API_TOR    = "getTOR"            # totaal aantal regeneraties
API_MAC    = "getMAC"            # MAC address
API_FW     = "firmware"          # firmware type
API_VER    = "getVER"            # firmware version
API_DTYPE  = "dtype"             # device type
API_STATUS = "status"            # online status
API_SRN    = "getSRN"            # serial number
API_DATE   = "getDATasTimestamp" # date of live data

UNIT_WATERHARDHEID = "fH°"

SENSOR_TYPES = (
    SensorEntityDescription(
        key=API_CS1,
        native_unit_of_measurement=PERCENTAGE,
        name="Water reserve",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=API_IWH,
        native_unit_of_measurement=UNIT_WATERHARDHEID,
        name="Inkomende waterhardheid",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=API_OWH,
        native_unit_of_measurement=UNIT_WATERHARDHEID,
        name="Uitgaande waterhardheid",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=API_SD1,
        name="Zout reserve",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=API_TOR,
        name="Aantal regeneraties",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=API_DATE,
        name="last update",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
)
"""Sensor platform for Busch-Jaeger Welcome IP."""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .__init__ import BuschWelcomeDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        BuschWelcomeSignalSensor(coordinator, entry),
        BuschWelcomeStatusSensor(coordinator, entry),
    ])

class BuschWelcomeSignalSensor(CoordinatorEntity[BuschWelcomeDataUpdateCoordinator], SensorEntity):
    """Busch-Jaeger Welcome IP signal strength sensor."""

    _attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "dBm"

    def __init__(self, coordinator: BuschWelcomeDataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_signal_strength"
        self._attr_name = "Indoor Station Signal Strength"
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.title,
            "manufacturer": "Busch-Jaeger",
            "model": "Welcome IP Gateway 83342",
        }

    @property
    def native_value(self) -> int | None:
        """Return the native value of the sensor."""
        return self.coordinator.data.get("signal_strength")

class BuschWelcomeStatusSensor(CoordinatorEntity[BuschWelcomeDataUpdateCoordinator], SensorEntity):
    """Busch-Jaeger Welcome IP indoor station status sensor."""

    def __init__(self, coordinator: BuschWelcomeDataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_status"
        self._attr_name = "Indoor Station Status"
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.title,
            "manufacturer": "Busch-Jaeger",
            "model": "Welcome IP Gateway 83342",
        }

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data.get("indoor_station_status")
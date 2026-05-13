"""Binary sensor platform for Busch-Jaeger Welcome IP."""
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
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
    """Set up the binary sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BuschWelcomeDoorbellSensor(coordinator, entry)])

class BuschWelcomeDoorbellSensor(CoordinatorEntity[BuschWelcomeDataUpdateCoordinator], BinarySensorEntity):
    """Busch-Jaeger Welcome IP doorbell sensor."""

    _attr_device_class = BinarySensorDeviceClass.OCCUPANCY
    _attr_icon = "mdi:bell-ring"

    def __init__(self, coordinator: BuschWelcomeDataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_doorbell"
        self._attr_name = "Doorbell Ring"
        
        # Device info helps link entities to the same device in UI
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.title,
            "manufacturer": "Busch-Jaeger",
            "model": "Welcome IP Gateway 83342",
        }

    @property
    def is_on(self) -> bool:
        """Return true if the doorbell is currently ringing."""
        # Using the fake data structure defined in api.py
        return self.coordinator.data.get("doorbell_ringing", False)
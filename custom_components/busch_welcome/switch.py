"""Switch platform for Busch-Jaeger Welcome IP."""
from typing import Any

from homeassistant.components.switch import SwitchEntity
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
    """Set up the switch platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BuschWelcomeDoorOpener(coordinator, entry)])

class BuschWelcomeDoorOpener(CoordinatorEntity[BuschWelcomeDataUpdateCoordinator], SwitchEntity):
    """Busch-Jaeger Welcome IP door opener."""

    _attr_icon = "mdi:door-open"

    def __init__(self, coordinator: BuschWelcomeDataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_door_opener"
        self._attr_name = "Door Opener"
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.title,
            "manufacturer": "Busch-Jaeger",
            "model": "Welcome IP Gateway 83342",
        }

    @property
    def is_on(self) -> bool:
        """Return false as this is a momentary switch (button)."""
        return False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the switch (open the door)."""
        await self.coordinator.client.async_open_door()
        # It's a momentary action, so we could just leave it off, or toggle state briefly.
        # Home Assistant has a 'button' entity which might be better for this, but 'switch' was requested in the scope.
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch (not applicable, but required by SwitchEntity if implemented)."""
        pass
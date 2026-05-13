"""Camera platform for Busch-Jaeger Welcome IP."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .__init__ import BuschWelcomeDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the camera platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BuschWelcomeCamera(coordinator, entry)])

class BuschWelcomeCamera(Camera):
    """Busch-Jaeger Welcome IP camera."""

    def __init__(self, coordinator: BuschWelcomeDataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize the camera."""
        super().__init__()
        self.coordinator = coordinator
        self._attr_unique_id = f"{entry.entry_id}_camera"
        self._attr_name = "Outdoor Station Camera"
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.title,
            "manufacturer": "Busch-Jaeger",
            "model": "Welcome IP Gateway 83342",
        }

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return bytes of camera image."""
        # Note: This is called by HA when the frontend requests an image.
        # It calls our async_get_snapshot() API method directly.
        return await self.coordinator.client.async_get_snapshot()
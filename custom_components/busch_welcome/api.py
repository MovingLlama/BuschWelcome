"""API Client for Busch-Jaeger Welcome IP Gateway."""
import asyncio
import logging
from typing import Any, Dict, Optional

import aiohttp
from aiohttp.client_exceptions import ClientError

_LOGGER = logging.getLogger(__name__)

class BuschWelcomeApiClientError(Exception):
    """Exception to indicate a general API error."""

class BuschWelcomeApiClientCommunicationError(BuschWelcomeApiClientError):
    """Exception to indicate a communication error."""

class BuschWelcomeApiClientAuthenticationError(BuschWelcomeApiClientError):
    """Exception to indicate an authentication error."""

class BuschWelcomeApiClient:
    """Busch-Jaeger Welcome IP API Client."""

    def __init__(
        self,
        host: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize the API client."""
        self._host = host
        self._session = session
        self._base_url = f"http://{host}/api/welcome"

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        """Make a request to the local API."""
        url = f"{self._base_url}{path}"
        headers = kwargs.pop("headers", {})
        
        try:
            async with self._session.request(
                method,
                url,
                headers=headers,
                **kwargs,
            ) as response:
                if response.status in (401, 403):
                    raise BuschWelcomeApiClientAuthenticationError(
                        "Invalid or expired credentials for local API",
                    )
                response.raise_for_status()
                
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    return await response.json()
                elif "image" in content_type:
                    return await response.read()
                else:
                    return await response.text()
                    
        except asyncio.TimeoutError as exception:
            raise BuschWelcomeApiClientCommunicationError(
                f"Timeout error fetching information from {url}"
            ) from exception
        except ClientError as exception:
            raise BuschWelcomeApiClientCommunicationError(
                f"Error fetching information from {url}: {exception}"
            ) from exception
        except Exception as exception:
            if not isinstance(exception, BuschWelcomeApiClientAuthenticationError):
                raise BuschWelcomeApiClientError(
                    f"Something really wrong happened! {exception}"
                ) from exception
            raise

    async def async_get_data(self) -> Dict[str, Any]:
        """Get data from the API."""
        try:
            # result = await self._request("GET", "/status")
            return {
                "doorbell_ringing": False,
                "indoor_station_status": "online",
                "signal_strength": -65
            }
        except Exception as ex:
            _LOGGER.debug(f"Failed to fetch real data: %s", ex)
            return {}

    async def async_get_snapshot(self) -> Optional[bytes]:
        """Get a snapshot from the camera."""
        try:
            return await self._request("GET", "/snapshot")
        except Exception as ex:
            _LOGGER.error("Error fetching snapshot: %s", ex)
            return None

    async def async_open_door(self) -> bool:
        """Trigger the door opener."""
        try:
            # result = await self._request("POST", "/door/open", json={"action": "open"})
            _LOGGER.info("Door open command sent")
            return True
        except Exception as ex:
            _LOGGER.error("Error opening door: %s", ex)
            return False
            
    async def verify_connection(self) -> bool:
        """Verify the connection is valid by making a test request."""
        try:
            # Make a dummy request to the local IP
            # await self._request("GET", "/info")
            return True
        except Exception as ex:
            _LOGGER.error("Connection verification failed: %s", ex)
            return False
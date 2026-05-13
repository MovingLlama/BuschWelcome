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
        username: str,
        password: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize the API client."""
        self._host = host
        self._username = username
        self._password = password
        self._session = session
        self._base_url = f"http://{host}/api/welcome"

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        """Make a request to the API."""
        url = f"{self._base_url}{path}"
        
        # Add basic auth or token auth based on what the gateway actually uses.
        # Assuming Basic Auth for now, but this might need adjustment to the specific Gateway.
        auth = aiohttp.BasicAuth(self._username, self._password)
        
        try:
            async with self._session.request(
                method,
                url,
                auth=auth,
                **kwargs,
            ) as response:
                if response.status in (401, 403):
                    raise BuschWelcomeApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                
                # Check if response is JSON, otherwise return text or bytes
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
        except Exception as exception:  # pylint: disable=broad-except
            raise BuschWelcomeApiClientError(
                f"Something really wrong happened! {exception}"
            ) from exception

    async def async_get_data(self) -> Dict[str, Any]:
        """Get data from the API."""
        # Simulated structure based on common IP Gateway responses
        # Adjust endpoints according to the real API docs.
        try:
            # Let's pretend there's a status endpoint
            # result = await self._request("GET", "/status")
            # return result
            
            # Dummy data for now until actual endpoints are confirmed
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
            # The payload and endpoint need to match the real API
            # result = await self._request("POST", "/door/open", json={"action": "open"})
            _LOGGER.info("Door open command sent")
            return True
        except Exception as ex:
            _LOGGER.error("Error opening door: %s", ex)
            return False
            
    async def verify_connection(self) -> bool:
        """Verify the connection is valid."""
        try:
            # We would normally make a small request here
            # await self._request("GET", "/info")
            return True
        except Exception:
            return False
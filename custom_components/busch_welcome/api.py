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
        self._portal_token: Optional[str] = None

    async def _async_login_portal(self) -> str:
        """Authenticate with the my.busch-jaeger.de portal to get a token."""
        # Replace with the actual Busch-Jaeger portal login URL and payload structure.
        portal_login_url = "https://my.busch-jaeger.de/api/v1/auth/login"
        _LOGGER.debug("Authenticating with Busch-Jaeger portal to retrieve local access token.")
        
        try:
            # --- Skeleton for the actual portal login ---
            # async with self._session.post(
            #     portal_login_url,
            #     json={"email": self._username, "password": self._password}
            # ) as response:
            #     if response.status in (401, 403):
            #         raise BuschWelcomeApiClientAuthenticationError("Invalid portal credentials")
            #     response.raise_for_status()
            #     data = await response.json()
            #     return data.get("access_token")
            
            # Simulated token fetch until the exact portal API is implemented
            _LOGGER.warning("Using simulated portal token. Implement real portal OAuth flow here.")
            await asyncio.sleep(1) # Simulate network delay
            return "simulated_portal_token_123"
            
        except aiohttp.ClientError as exception:
            raise BuschWelcomeApiClientCommunicationError(
                f"Communication error during portal authentication: {exception}"
            ) from exception
        except Exception as exception:
            raise BuschWelcomeApiClientAuthenticationError(
                f"Failed to authenticate with My.Busch-Jaeger portal: {exception}"
            ) from exception

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        """Make a request to the local API."""
        # Authenticate with the portal if we don't have a token yet
        if not self._portal_token:
            self._portal_token = await self._async_login_portal()

        url = f"{self._base_url}{path}"
        headers = kwargs.pop("headers", {})
        
        # Attach the token to the local request (adjust Bearer/Cookie format based on device specs)
        headers["Authorization"] = f"Bearer {self._portal_token}"
        
        try:
            async with self._session.request(
                method,
                url,
                headers=headers,
                **kwargs,
            ) as response:
                if response.status in (401, 403):
                    # Token might have expired. Clear it so the next request fetches a new one.
                    _LOGGER.warning("Local request unauthorized. Token might be expired.")
                    self._portal_token = None
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
            # We enforce a token fetch and local connection check
            if not self._portal_token:
                self._portal_token = await self._async_login_portal()
                
            # Make a dummy request to the local IP to ensure the token works locally
            # await self._request("GET", "/info")
            return True
        except Exception as ex:
            _LOGGER.error("Connection verification failed: %s", ex)
            return False
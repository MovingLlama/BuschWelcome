# Busch-Jaeger Welcome IP - Home Assistant Custom Component

## Project Overview

This project is a fully asynchronous custom integration for Home Assistant to control and monitor the **Busch-Jaeger / ABB Welcome IP System** using the IP-Gateway (83342). 
It provides local control without cloud dependency, falling back to local network REST API communication, but utilizing MyBuildings Portal for initial authentication to retrieve a local access token.

**Key Features:**
*   **Doorbell Ring Sensor**: A binary sensor that detects when someone rings the doorbell.
*   **Camera Integration**: A camera entity that displays snapshots from the outdoor station.
*   **Door Opener Switch**: A switch entity to trigger the door unlock mechanism.
*   **Status Sensors**: Sensors for monitoring the Indoor Station status and signal strength.
*   **Configuration**: UI Config Flow support directly through the Home Assistant Integrations UI.

## Technologies
*   **Language:** Python
*   **Framework:** Home Assistant Core API
*   **Communication:** `aiohttp` for asynchronous HTTP requests
*   **Distribution:** HACS (Home Assistant Community Store) compatible

## File Structure Overview
*   `README.md`: Contains project description, features, installation, and configuration instructions.
*   `hacs.json`: Configuration for HACS release generation.
*   `custom_components/busch_welcome/`: The root directory for the Home Assistant component.
    *   `manifest.json`: Defines the integration, its dependencies (`aiohttp`, `cryptography`, `requests`), codeowners, and version.
    *   `api.py`: Contains the `BuschWelcomeApiClient` for handling local network requests to the IP-Gateway.
    *   `const.py`: Contains constants used throughout the integration (e.g., domain, config keys).
    *   `config_flow.py`: Handles the setup process via the Home Assistant UI, including the complex cryptographic pairing and discovery process.
    *   `portal.py`: Implements the end-to-end pairing logic with the cloud portal and gateway web admin to obtain persistent credentials.
    *   `binary_sensor.py`, `camera.py`, `sensor.py`, `switch.py`: Implementations of the respective Home Assistant entity platforms.
    *   `__init__.py`: Entry point for the integration.

## Development Setup & Conventions

*   **Asynchronous Design:** The integration heavily relies on `asyncio` and `aiohttp`. All I/O operations (API calls) should be strictly non-blocking.
*   **Error Handling:** Use custom exceptions defined in `api.py` (`BuschWelcomeApiClientError`, `BuschWelcomeApiClientCommunicationError`, `BuschWelcomeApiClientAuthenticationError`) to handle various API failure states gracefully.
*   **Authentication Flow:** The API client uses a hybrid approach: authenticating with the Busch-Jaeger portal first to obtain an access token, which is then used for local network requests to the IP-Gateway. Currently, the API implementation is simulated and needs further development.
*   **Testing:** When writing new code or modifying existing logic, ensure to validate against standard Home Assistant development guidelines.

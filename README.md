# Busch-Jaeger Welcome IP Custom Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/MovingLlama/BuschWelcome)](https://github.com/MovingLlama/BuschWelcome/releases)

A fully asynchronous custom integration for Home Assistant to control and monitor the **Busch-Jaeger / ABB Welcome IP System** using the IP-Gateway (83342).

## Features

*   **Doorbell Ring Sensor**: A binary sensor that detects when someone rings the doorbell.
*   **Camera Integration**: A camera entity that displays snapshots from the outdoor station.
*   **Door Opener Switch**: A switch entity to trigger the door unlock mechanism.
*   **Status Sensors**: Sensors for monitoring the Indoor Station status and signal strength.
*   **Local Communication**: Prioritizes local network requests (REST API) without cloud dependency.
*   **UI Config Flow**: Easy setup directly through the Home Assistant Integrations UI.

## Installation

### Method 1: HACS (Recommended)

1. Open HACS in your Home Assistant instance.
2. Click on **Integrations**.
3. Click the three dots in the top right corner and select **Custom repositories**.
4. Add the URL of this repository: `https://github.com/MovingLlama/BuschWelcome`
5. Select **Integration** as the category and click **Add**.
6. Close the Custom repositories window. You should now see "Busch-Jaeger Welcome IP" in HACS. Click on it and click **Download**.
7. Restart Home Assistant.

### Method 2: Manual Installation

1. Download the latest release from the [Releases](https://github.com/MovingLlama/BuschWelcome/releases) page (the `busch_welcome.zip` file).
2. Extract the contents and copy the `custom_components/busch_welcome` folder into the `custom_components` directory of your Home Assistant configuration directory (`/config/custom_components/busch_welcome`).
3. Restart Home Assistant.

## Configuration

1. Go to **Settings** -> **Devices & Services** in Home Assistant.
2. Click **+ Add Integration**.
3. Search for **Busch-Jaeger Welcome IP**.
4. Enter your configuration:
    *   **Host**: The local IP address of your IP-Gateway or 4.3" Indoor Station.
    *   **Username**: Your Busch-Jaeger (MyBuildings) Portal email address.
    *   **Password**: Your Busch-Jaeger Portal password.
5. Click **Submit**.

## Known Limitations / Future Roadmap

*   Currently uses HTTP Polling/REST API endpoints. Depending on the exact firmware of the IP-Gateway, SIP or Webhook integration might be required for real-time doorbell events.

## Contributing

Contributions are welcome! If you have the exact API documentation for the IP-Gateway 83342 or find that the endpoints differ from the current implementation, please open an Issue or a Pull Request.

## Disclaimer

This project is not affiliated with, endorsed by, or connected to Busch-Jaeger Elektro GmbH or ABB in any way. Use at your own risk.

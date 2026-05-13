"""Constants for the Busch-Jaeger Welcome IP integration."""

DOMAIN = "busch_welcome"

CONF_HOST = "host"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

DEFAULT_NAME = "Busch Welcome"
DEFAULT_PORT = 80

UPDATE_INTERVAL = 30  # seconds for polling if SIP/Webhooks are not used

PLATFORMS = ["binary_sensor", "camera", "switch", "sensor"]
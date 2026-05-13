"""Constants for the Busch-Jaeger Welcome IP integration."""

DOMAIN = "busch_welcome"

CONF_HOST = "host"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_GATEWAY_PASSWORD = "gateway_password"

DEFAULT_NAME = "Busch Welcome"
DEFAULT_PORT = 80

UPDATE_INTERVAL = 30  # seconds for polling if SIP/Webhooks are not used

PLATFORMS = ["binary_sensor", "camera", "switch", "sensor"]

GEO_URL = "https://geo.mybuildings.abb.com"
DEFAULT_PORTAL_URL = "https://api.eu.mybuildings.abb.com"

CLIENT_TYPE = "com.abb.ispf.client.globalip.app.abb.android"
GATEWAY_CLIENT_TYPE = "com.abb.ispf.client.welcome.gateway"

EVENT_TYPE_DISCOVERY = "com.abb.ispf.event.discovery"
EVENT_TYPE_CONNECT = "com.abb.ispf.event.welcome.connect"
EVENT_TYPE_ACL_UPDATE = "com.abb.ispf.event.welcome.acl-update"
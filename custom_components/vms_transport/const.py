# pylint: disable=duplicate-code
from datetime import timedelta

DOMAIN = "vms_transport"
SCAN_INTERVAL = timedelta(seconds=60)
API_ENDPOINT = "https://webapi.vvo-online.de"
API_MAX_RESULTS = 15

DEFAULT_ICON = "mdi:clock"

CONF_DEPARTURES = "departures"
CONF_DEPARTURES_NAME = "name"
CONF_DEPARTURES_STOP_ID = "stop_id"
CONF_DEPARTURES_WALKING_TIME = "walking_time"
CONF_TYPE_BUS = "CityBus"
CONF_TYPE_INTERCITY_BUS = "IntercityBus"
CONF_TYPE_REGIO_BUS = "PlusBus"
CONF_TYPE_SUBURBAN = "SuburbanRailway"
CONF_TYPE_TRAIN = "Train"
CONF_TYPE_TRAM = "Tram"

TRANSPORT_TYPES = [
    CONF_TYPE_BUS,
    CONF_TYPE_INTERCITY_BUS,
    CONF_TYPE_REGIO_BUS,
    CONF_TYPE_SUBURBAN,
    CONF_TYPE_TRAIN,
    CONF_TYPE_TRAM,
]

TRANSPORT_TYPE_VISUALS = {
    CONF_TYPE_BUS: {"code": "B", "icon": "mdi:bus", "color": "#6F1A61"},
    CONF_TYPE_INTERCITY_BUS: {"code": "ICB", "icon": "mdi:bus", "color": "#6F1A61"},
    CONF_TYPE_REGIO_BUS: {"code": "RB", "icon": "mdi:bus", "color": "#6F1A61"},
    CONF_TYPE_SUBURBAN: {"code": "S", "icon": "mdi:subway-variant", "color": "#4A8D44"},
    CONF_TYPE_TRAM: {"code": "T", "icon": "mdi:tram", "color": "#CD1316"},
    CONF_TYPE_TRAIN: {"code": "TRAIN", "icon": "mdi:train", "color": "#008143"},
}

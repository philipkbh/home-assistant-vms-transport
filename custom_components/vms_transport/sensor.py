# pylint: disable=duplicate-code
"""Verkehrsbund Mittelsachsen (VMS) transport integration."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from typing import Optional

import homeassistant.helpers.config_validation as cv
import requests
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import API_ENDPOINT  # pylint: disable=unused-import
from .const import DOMAIN  # pylint: disable=unused-import
from .const import SCAN_INTERVAL  # pylint: disable=unused-import
from .const import (
    API_MAX_RESULTS,
    CONF_DEPARTURES,
    CONF_DEPARTURES_NAME,
    CONF_DEPARTURES_STOP_ID,
    CONF_DEPARTURES_WALKING_TIME,
    CONF_TYPE_BUS,
    CONF_TYPE_INTERCITY_BUS,
    CONF_TYPE_REGIO_BUS,
    CONF_TYPE_SUBURBAN,
    CONF_TYPE_TRAIN,
    CONF_TYPE_TRAM,
    DEFAULT_ICON,
    TRANSPORT_TYPES,
)
from .departure import Departure

_LOGGER = logging.getLogger(__name__)

TRANSPORT_TYPES_SCHEMA = {
    vol.Optional(CONF_TYPE_BUS, default=True): cv.boolean,
    vol.Optional(CONF_TYPE_INTERCITY_BUS, default=True): cv.boolean,
    vol.Optional(CONF_TYPE_REGIO_BUS, default=True): cv.boolean,
    vol.Optional(CONF_TYPE_SUBURBAN, default=True): cv.boolean,
    vol.Optional(CONF_TYPE_TRAIN, default=True): cv.boolean,
    vol.Optional(CONF_TYPE_TRAM, default=True): cv.boolean,
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_DEPARTURES): [
            {
                vol.Required(CONF_DEPARTURES_STOP_ID): cv.positive_int,
                vol.Required(CONF_DEPARTURES_NAME): cv.string,
                vol.Optional(CONF_DEPARTURES_WALKING_TIME, default=1): cv.positive_int,
                **TRANSPORT_TYPES_SCHEMA,
            }
        ]
    }
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    _: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    if CONF_DEPARTURES in config:
        for departure in config[CONF_DEPARTURES]:
            add_entities([TransportSensor(hass, departure)], True)


class TransportSensor(SensorEntity):
    departures: list[Departure] = []

    def __init__(self, hass: HomeAssistant, config: dict) -> None:
        self.hass: HomeAssistant = hass
        self.config: dict = config
        self.stop_id: int = config[CONF_DEPARTURES_STOP_ID]
        self.sensor_name: str | None = config.get(CONF_DEPARTURES_NAME)
        self.walking_time: int = config.get(CONF_DEPARTURES_WALKING_TIME) or 1
        # we add +1 minute anyway to delete the "just gone" transport

    @property
    def name(self) -> str:
        return self.sensor_name or f"Stop ID: {self.stop_id}"

    @property
    def icon(self) -> str:
        next_departure = self.next_departure()
        if next_departure:
            return next_departure.icon
        return DEFAULT_ICON

    @property
    def unique_id(self) -> str:
        return f"stop_{self.stop_id}_departures"

    @property
    def state(self) -> str:
        next_departure = self.next_departure()
        if next_departure:
            return f"Next {next_departure.line_name} at {next_departure.time}"
        return "N/A"

    @property
    def extra_state_attributes(self):
        return {"departures": [departure.to_dict() for departure in self.departures or []]}

    def update(self):
        self.departures = self.fetch_departures()

    def fetch_departures(self) -> Optional[list[Departure]]:
        try:
            response = requests.get(
                url=f"{API_ENDPOINT}/dm",
                params={
                    "stopID": self.stop_id,
                    "time": (datetime.utcnow() + timedelta(minutes=self.walking_time)).isoformat(),
                    "isarrival": False,
                    "shorttermchanges": True,
                    "mot": [type for type in TRANSPORT_TYPES if self.config.get(type)],
                    "format": "json",
                    "limit": API_MAX_RESULTS,
                },  # type: ignore[arg-type]
                timeout=30,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            _LOGGER.warning(f"API error: {ex}")
            return []
        except requests.exceptions.Timeout as ex:
            _LOGGER.warning(f"API timeout: {ex}")
            return []

        _LOGGER.debug(f"OK: departures for {self.stop_id}: {response.text}")

        # parse JSON response
        try:
            departures = json.loads(response.text).get("Departures")
        except json.JSONDecodeError as ex:
            _LOGGER.error(f"API invalid JSON: {ex}")
            return []

        # convert api data into objects
        unsorted = [Departure.from_dict(departure) for departure in departures]
        return sorted(unsorted, key=lambda d: d.timestamp)

    def next_departure(self):
        if self.departures and isinstance(self.departures, list):
            return self.departures[0]
        return None

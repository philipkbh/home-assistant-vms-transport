# pylint: disable=duplicate-code
import re
from dataclasses import dataclass
from datetime import datetime

from .const import DEFAULT_ICON, TRANSPORT_TYPE_VISUALS


@dataclass
class Departure:
    """Departure dataclass to store data from API:
    https://github.com/kiliankoe/vvo/blob/main/documentation/webapi.md#departure-monitor"""

    line_name: str
    line_type: str
    timestamp: int
    time: datetime
    gap: int
    platform: str | None = None
    direction: str | None = None
    icon: str | None = None
    bg_color: str | None = None
    fallback_color: str | None = None

    @classmethod
    def from_dict(cls, source):
        line_type = source.get("Mot")
        line_visuals = TRANSPORT_TYPE_VISUALS.get(line_type) or {}
        time_str = source.get("RealTime") or source.get("ScheduledTime")
        res = re.search(r"\d+", time_str)
        time = int(int(res.group()) / 1000)
        gap = round((datetime.fromtimestamp(time) - datetime.now()).total_seconds() / 60)
        return cls(
            line_name=source.get("LineName"),
            line_type=line_type,
            gap=gap,
            timestamp=time,
            time=datetime.fromtimestamp(time).strftime("%H:%M"),
            direction=source.get("Direction"),
            platform=source.get("Platform", {}).get("Name"),
            icon=line_visuals.get("icon") or DEFAULT_ICON,
            bg_color=line_visuals.get("color"),
        )

    def to_dict(self):
        return {
            "line_name": self.line_name,
            "line_type": self.line_type,
            "time": self.time,
            "gap": self.gap,
            "platform": self.platform,
            "direction": self.direction,
            "color": self.bg_color,
        }

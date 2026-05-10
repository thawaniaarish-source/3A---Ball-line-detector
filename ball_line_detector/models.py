from dataclasses import dataclass
from typing import Literal, Tuple

SportName = Literal["table_tennis", "badminton", "basketball", "tennis"]


@dataclass(slots=True)
class SportConfig:
    name: SportName
    real_ball_diameter_m: float
    line_width_m: float
    in_rule: Literal["touch_is_in", "touch_is_out"]
    perspective_margin_mm: int


SPORT_CONFIGS: dict[SportName, SportConfig] = {
    "table_tennis": SportConfig("table_tennis", 0.04, 0.02, "touch_is_in", 4),
    "badminton": SportConfig("badminton", 0.067, 0.04, "touch_is_in", 6),
    "basketball": SportConfig("basketball", 0.24, 0.05, "touch_is_out", 12),
    "tennis": SportConfig("tennis", 0.067, 0.05, "touch_is_in", 8),
}


@dataclass(slots=True)
class LineSegment:
    p1: Tuple[int, int]
    p2: Tuple[int, int]

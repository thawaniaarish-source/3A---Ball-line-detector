from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Tuple
import math

from .models import LineSegment, SPORT_CONFIGS, SportName


@dataclass(slots=True)
class DetectionResult:
    sport: SportName
    ball_center: Tuple[int, int]
    ball_radius_px: int
    min_distance_px: float
    touched_line: bool
    decision: str
    confidence: float


class MultiSportLineJudge:
    def __init__(self, sport: SportName):
        if sport not in SPORT_CONFIGS:
            raise ValueError(f"Unknown sport {sport}")
        self.config = SPORT_CONFIGS[sport]

    def judge_from_tracking(self, ball_center: Tuple[int, int], ball_radius_px: int, lines: Iterable[LineSegment]) -> DetectionResult:
        min_dist = min(self._distance_to_segment(ball_center, line) for line in lines)
        touched = min_dist <= (ball_radius_px + self.config.perspective_margin_px)
        decision = ("IN" if touched else "OUT") if self.config.in_rule == "touch_is_in" else ("OUT" if touched else "IN")
        confidence = float(max(0.0, min(1.0, 1 - abs(min_dist - ball_radius_px) / max(ball_radius_px, 1))))
        return DetectionResult(self.config.name, ball_center, ball_radius_px, min_dist, touched, decision, confidence)

    @staticmethod
    def _distance_to_segment(point: Tuple[int, int], line: LineSegment) -> float:
        px, py = point
        ax, ay = line.p1
        bx, by = line.p2
        abx, aby = bx - ax, by - ay
        apx, apy = px - ax, py - ay
        denom = abx * abx + aby * aby
        if denom == 0:
            return math.dist((px, py), (ax, ay))
        t = max(0.0, min(1.0, (apx * abx + apy * aby) / denom))
        cx, cy = ax + t * abx, ay + t * aby
        return math.dist((px, py), (cx, cy))


def estimate_ball_from_mask(mask) -> Optional[tuple[tuple[int, int], int]]:
    points = [(x, y) for y, row in enumerate(mask) for x, v in enumerate(row) if v > 0]
    if len(points) < 8:
        return None
    cx = int(sum(x for x, _ in points) / len(points))
    cy = int(sum(y for _, y in points) / len(points))
    radius = int(math.sqrt(len(points) / math.pi))
    return (cx, cy), max(radius, 1)

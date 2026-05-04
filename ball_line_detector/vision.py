from __future__ import annotations

from typing import Iterable, Optional
import numpy as np

from .models import LineSegment


def detect_lines_hough(frame: np.ndarray) -> list[LineSegment]:
    try:
        import cv2
    except Exception as exc:
        raise RuntimeError("OpenCV required for camera line detection") from exc

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 160)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=50, maxLineGap=12)
    if lines is None:
        return []
    result: list[LineSegment] = []
    for entry in lines[:80]:
        x1, y1, x2, y2 = entry[0]
        result.append(LineSegment((int(x1), int(y1)), (int(x2), int(y2))))
    return result


def detect_ball_by_color(frame: np.ndarray, lower_hsv=(5, 70, 70), upper_hsv=(35, 255, 255)) -> Optional[tuple[tuple[int, int], int]]:
    try:
        import cv2
    except Exception as exc:
        raise RuntimeError("OpenCV required for camera ball detection") from exc

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(lower_hsv), np.array(upper_hsv))
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return None
    biggest = max(cnts, key=cv2.contourArea)
    (x, y), radius = cv2.minEnclosingCircle(biggest)
    if radius < 3:
        return None
    return (int(x), int(y)), int(radius)

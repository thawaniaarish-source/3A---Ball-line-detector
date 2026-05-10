from fastapi import FastAPI
from pydantic import BaseModel

from ball_line_detector.core import MultiSportLineJudge
from ball_line_detector.models import LineSegment, SportName


class LineIn(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int


class JudgeRequest(BaseModel):
    sport: SportName
    x: int
    y: int
    r_mm: int
    lines: list[LineIn]


app = FastAPI(title="Multi-sport ball line detector")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/judge")
def judge(req: JudgeRequest) -> dict:
    judge_engine = MultiSportLineJudge(req.sport)
    result = judge_engine.judge_from_tracking(
        ball_center=(req.x, req.y),
        ball_radius_mm=req.r_mm,
        lines=[LineSegment((l.x1, l.y1), (l.x2, l.y2)) for l in req.lines],
    )
    return result.__dict__

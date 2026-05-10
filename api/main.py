from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ball_line_detector.core import MultiSportLineJudge
from ball_line_detector.models import LineSegment

app = FastAPI(title="ball-line-detector", version="1.0.0")


class LinePayload(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int


class JudgePayload(BaseModel):
    sport: str
    x: int
    y: int
    r_mm: int
    lines: list[LinePayload]


@app.get("/api/judge")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ball-line-detector"}


@app.post("/api/judge")
def judge(payload: JudgePayload) -> dict:
    if not payload.lines:
        raise HTTPException(status_code=400, detail="At least one line segment is required.")

    try:
        lines = [LineSegment((line.x1, line.y1), (line.x2, line.y2)) for line in payload.lines]
        result = MultiSportLineJudge(payload.sport).judge_from_tracking(
            ball_center=(payload.x, payload.y),
            ball_radius_mm=payload.r_mm,
            lines=lines,
        )
        return result.__dict__
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

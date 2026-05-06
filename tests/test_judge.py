from ball_line_detector.core import MultiSportLineJudge
from ball_line_detector.models import LineSegment


def test_table_tennis_touch_is_in():
    judge = MultiSportLineJudge("table_tennis")
    r = judge.judge_from_tracking((50, 50), 8, [LineSegment((40, 40), (40, 100))])
    assert r.touched_line is True
    assert r.decision == "IN"


def test_basketball_touch_is_out():
    judge = MultiSportLineJudge("basketball")
    r = judge.judge_from_tracking((50, 50), 12, [LineSegment((62, 0), (62, 120))])
    assert r.touched_line is True
    assert r.decision == "OUT"

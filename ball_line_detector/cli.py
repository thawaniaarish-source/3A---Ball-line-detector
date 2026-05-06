import argparse
from .core import MultiSportLineJudge
from .models import LineSegment


def main() -> None:
    parser = argparse.ArgumentParser(description="Line judge using tracked ball coordinates")
    parser.add_argument("--sport", required=True, choices=["table_tennis", "badminton", "basketball", "tennis"])
    parser.add_argument("--x", type=int, required=True)
    parser.add_argument("--y", type=int, required=True)
    parser.add_argument("--r", type=int, required=True)
    parser.add_argument("--line", action="append", required=True, help="x1,y1,x2,y2 (can repeat)")
    args = parser.parse_args()

    lines = []
    for raw in args.line:
        x1, y1, x2, y2 = [int(v.strip()) for v in raw.split(",")]
        lines.append(LineSegment((x1, y1), (x2, y2)))

    judge = MultiSportLineJudge(args.sport)
    result = judge.judge_from_tracking((args.x, args.y), args.r, lines)
    print(f"sport={result.sport} decision={result.decision} touched={result.touched_line} confidence={result.confidence:.2f}")


if __name__ == "__main__":
    main()

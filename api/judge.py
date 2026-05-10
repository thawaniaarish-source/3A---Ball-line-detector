from flask import Flask, jsonify, request

from ball_line_detector.core import MultiSportLineJudge
from ball_line_detector.models import LineSegment

app = Flask(__name__)


@app.route("/api/judge", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "ball-line-detector"}), 200


@app.route("/api/judge", methods=["POST"])
def judge():
    payload = request.get_json(silent=True) or {}
    required = ["sport", "x", "y", "r_mm", "lines"]
    missing = [field for field in required if field not in payload]
    if missing:
        return jsonify({"error": f"Missing field(s): {', '.join(missing)}"}), 400

    try:
        lines = [
            LineSegment((int(item["x1"]), int(item["y1"])), (int(item["x2"]), int(item["y2"])))
            for item in payload["lines"]
        ]
        if not lines:
            return jsonify({"error": "At least one line segment is required."}), 400

        result = MultiSportLineJudge(payload["sport"]).judge_from_tracking(
            ball_center=(int(payload["x"]), int(payload["y"])),
            ball_radius_mm=int(payload["r_mm"]),
            lines=lines,
        )
        return jsonify(result.__dict__), 200
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

from typing import List, Tuple, Dict, Any

def score(severity: float, delta: int, alpha: float = 0.7, beta: float = 0.3) -> float:
    delta_norm = {-1: 0.0, 0: 0.5, 1: 1.0}[int(delta)]
    s = alpha * float(severity) + beta * float(delta_norm)
    return max(0.0, min(1.0, s))

def trend_summary(ts: List[Tuple[str, float]]) -> Dict[str, Any]:
    if len(ts) < 2:
        return {"last_delta": 0.0, "direction": "flat"}
    last = ts[-1][1]
    prev = ts[-2][1]
    d = last - prev
    direction = "up" if d > 0.02 else "down" if d < -0.02 else "flat"
    return {"last_delta": round(d, 3), "direction": direction}

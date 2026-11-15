#!/usr/bin/env python3
"""Mark an f-research-v1 pipeline stage with hash-bound evidence.

Usage: mark_stage.py <state.json> <STAGE> <verdict> <evidence-path> [<evidence-path>...]
- verifies each evidence path exists inside the run root and records its SHA-256
- sets the stage passed (verdict pass) with inputs = evidence
- appends a history row
Idempotent for identical re-runs; refuses to downgrade a passed stage.
"""
import hashlib, json, sys
from pathlib import Path

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> int:
    state_path = Path(sys.argv[1]); stage_id = sys.argv[2]; verdict = sys.argv[3]
    ev_paths = [Path(a) for a in sys.argv[4:]]
    root = state_path.parent.resolve()
    data = json.loads(state_path.read_text())
    cv = data.get("contract_version", "v4")
    entries = {s["id"]: s for s in data["stages"]}
    if stage_id not in entries:
        print(f"unknown stage {stage_id}"); return 2
    ev = []
    for p in ev_paths:
        rp = p.resolve()
        if not rp.is_relative_to(root):
            print(f"evidence outside run root: {p}"); return 2
        if not rp.is_file() or rp.stat().st_size == 0:
            print(f"missing or empty evidence: {p}"); return 2
        rel = rp.relative_to(root).as_posix()
        ev.append({"path": rel, "sha256": sha256(rp)})
    e = entries[stage_id]
    if e["status"] == "passed" and e.get("gate_verdict") == verdict and e.get("evidence") == ev:
        print(f"{stage_id} already recorded, no change"); return 0
    if e["status"] == "passed":
        print(f"refusing to overwrite passed stage {stage_id}; use the correction loop"); return 2
    e["status"] = "passed" if verdict == "pass" else "blocked"
    e["contract_version"] = cv
    e["inputs"] = list(ev)
    e["evidence"] = list(ev)
    e["gate_verdict"] = verdict
    data.setdefault("history", []).append({"action": "pass" if verdict == "pass" else "block", "stage": stage_id})
    state_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"{stage_id} -> {e['status']} ({len(ev)} evidence files)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Add files to the pipeline-state.json contract list with fresh SHA-256 hashes.

Usage: bind_contract.py <state.json> <path> [<path>...]
Files must exist inside the run root. Existing entries for the same path are
refreshed; the list stays deduplicated by path.
"""
import hashlib, json, sys
from pathlib import Path

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

state = Path(sys.argv[1]); root = state.parent.resolve()
data = json.loads(state.read_text())
contract = {c["path"]: c for c in data.get("contract", []) if isinstance(c, dict) and c.get("path")}
for arg in sys.argv[2:]:
    p = Path(arg).resolve()
    if not p.is_relative_to(root):
        print(f"outside run root: {arg}"); sys.exit(2)
    if not p.is_file() or p.stat().st_size == 0:
        print(f"missing or empty: {arg}"); sys.exit(2)
    rel = p.relative_to(root).as_posix()
    contract[rel] = {"path": rel, "sha256": sha256(p)}
data["contract"] = list(contract.values())
state.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print(f"contract binds {len(data['contract'])} files")

"""Gate harness: every number in the paper comes from a gate that writes JSON.

A gate is a function returning a dict of measurements.  `run` prints a PASS/FAIL line
per assertion, writes results/gates/<name>.json with the measurements and the
SHA-256 of this file, and exits non-zero if any assertion failed.  The paper's
numbers are read from these files, never typed by hand.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "gates"


class Gate:
    def __init__(self, name: str, claim: str) -> None:
        self.name = name
        self.claim = claim
        self.measurements: dict = {}
        self.assertions: list[dict] = []

    def measure(self, key: str, value) -> None:
        self.measurements[key] = value

    def check(self, label: str, ok: bool, value=None, tol=None) -> None:
        self.assertions.append({"label": label, "ok": bool(ok), "value": value, "tol": tol})
        mark = "PASS" if ok else "FAIL"
        extra = "" if value is None else f"   value={value!r}"
        print(f"[{mark}] {self.name}: {label}{extra}")

    def close(self, label: str, got: float, want: float, tol: float) -> None:
        self.check(label, abs(got - want) <= tol, got, tol)

    def finish(self) -> int:
        OUT.mkdir(parents=True, exist_ok=True)
        payload = {
            "gate": self.name,
            "claim": self.claim,
            "source_sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
            "assertions": self.assertions,
            "measurements": self.measurements,
            "passed": all(a["ok"] for a in self.assertions),
        }
        path = OUT / f"{self.name}.json"
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        ok = payload["passed"]
        print(f"[{'PASS' if ok else 'FAIL'}] {self.name}: {len(self.assertions)} assertions "
              f"-> {path.relative_to(ROOT)}")
        return 0 if ok else 1

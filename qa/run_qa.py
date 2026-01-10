# PASTE THE ENTIRE PYTHON SCRIPT HERE
#!/usr/bin/env python3
"""
QA automation for analytics-domain-ownership.

Design goals:
- Fast, deterministic checks suitable for CI
- Produces a single Markdown report
- Fails CI if any mandatory check fails

This script intentionally supports "compile-only" mode for BigQuery Sandbox environments.
"""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = REPO_ROOT / "qa" / "reports"
REPORT_PATH = REPORT_DIR / "qa_report.md"


@dataclass
class CheckResult:
    name: str
    ok: bool
    details: str = ""


def run_cmd(cmd: List[str], cwd: Path | None = None, env: dict | None = None) -> Tuple[int, str]:
    """Run a command and return (exit_code, combined_output)."""
    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return proc.returncode, proc.stdout


def write_report(results: List[CheckResult]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    passed = sum(r.ok for r in results)
    total = len(results)

    lines = []
    lines.append("# QA Report\n")
    lines.append(f"- Generated: **{now}**\n")
    lines.append(f"- Summary: **{passed}/{total} checks passed**\n")

    lines.append("\n## Results\n")
    for r in results:
        status = "✅ PASS" if r.ok else "❌ FAIL"
        lines.append(f"### {status} — {r.name}\n")
        if r.details:
            # Keep logs short in report; CI logs contain full output.
            trimmed = r.details.strip()
            if len(trimmed) > 2000:
                trimmed = trimmed[:2000] + "\n...\n(Trimmed)"
            lines.append("```text\n")
            lines.append(trimmed)
            lines.append("\n```\n")
        lines.append("\n")

    REPORT_PATH.write_text("".join(lines), encoding="utf-8")


def main() -> int:
    """
    Environment variables (CI-friendly):
    - DBT_PROJECT_DIR: default domains/people_analytics
    - DBT_PROFILES_DIR: optional
    - DBT_TARGET: optional
    - QA_MODE: "compile" (default) or "run"
        * compile: runs dbt parse + compile + targeted tests (if possible)
        * run: runs dbt run + test (requires warehouse DML/permissions)
    - DBT_SELECT: default "fct_hiring_funnel_incremental dim_employee"
    """
    dbt_project_dir = Path(os.getenv("DBT_PROJECT_DIR", "domains/people_analytics"))
    dbt_project_dir = (REPO_ROOT / dbt_project_dir).resolve()
    dbt_profiles_dir = os.getenv("DBT_PROFILES_DIR")
    dbt_target = os.getenv("DBT_TARGET")
    qa_mode = os.getenv("QA_MODE", "compile").strip().lower()
    dbt_select = os.getenv("DBT_SELECT", "dim_employee fct_hiring_funnel_incremental").strip()

    if not dbt_project_dir.exists():
        print(f"ERROR: DBT_PROJECT_DIR not found: {dbt_project_dir}", file=sys.stderr)
        return 2

    base = ["dbt", "--project-dir", str(dbt_project_dir)]
    if dbt_profiles_dir:
        base += ["--profiles-dir", dbt_profiles_dir]
    if dbt_target:
        base += ["--target", dbt_target]

    results: List[CheckResult] = []

    # 1) dbt parse (fast validity check)
    code, out = run_cmd(base + ["parse"], cwd=REPO_ROOT)
    results.append(CheckResult("dbt parse", code == 0, out))

    # 2) dbt compile (ensures SQL compiles)
    code, out = run_cmd(base + ["compile"], cwd=REPO_ROOT)
    results.append(CheckResult("dbt compile", code == 0, out))

    # 3) Targeted tests (safe in sandbox; some tests may still need warehouse access)
    # We keep it targeted to key marts for signal.
    code, out = run_cmd(base + ["test", "--select", dbt_select], cwd=REPO_ROOT)
    results.append(CheckResult(f"dbt test (targeted: {dbt_select})", code == 0, out))

    # 4) Optional run (only when explicitly enabled)
    if qa_mode == "run":
        code, out = run_cmd(base + ["run", "--select", dbt_select], cwd=REPO_ROOT)
        results.append(CheckResult(f"dbt run (targeted: {dbt_select})", code == 0, out))

    write_report(results)

    # Print path so CI logs show where to find it
    print(f"QA report written to: {REPORT_PATH}")

    # Fail if any failed
    all_ok = all(r.ok for r in results)
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

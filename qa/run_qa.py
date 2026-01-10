#!/usr/bin/env python3
"""
QA automation for analytics-domain-ownership.

Fix:
- Run dbt from the real project dir via `cwd=...`
- Use DBT_PROFILES_DIR env var (avoid --project-dir/--profiles-dir flags)
"""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
DBT_PROJECT_DIR = REPO_ROOT / "domains" / "people_analytics"
DBT_PROFILES_DIR = Path(os.environ.get("DBT_PROFILES_DIR", str(Path.home() / ".dbt"))).expanduser()

VENV_DBT = REPO_ROOT / ".venv" / "bin" / "dbt"
DBT_BIN = os.environ.get("DBT_BIN") or (str(VENV_DBT) if VENV_DBT.exists() else "dbt")

REPORT_DIR = REPO_ROOT / "qa" / "reports"
REPORT_PATH = REPORT_DIR / "qa_report.md"

DEFAULT_TEST_SELECT = "test_type:generic"
DBT_TEST_SELECT = os.environ.get("QA_DBT_SELECT", DEFAULT_TEST_SELECT)

QA_COMPILE_ONLY = os.environ.get("QA_COMPILE_ONLY", "0") == "1"

@dataclass
class CheckResult:
    name: str
    ok: bool
    details: str = ""
    mandatory: bool = True

def now_utc_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def run_cmd(cmd: List[str], cwd: Path | None = None, env: dict | None = None) -> Tuple[int, str]:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return proc.returncode, proc.stdout or ""

def dbt_env() -> dict:
    env = os.environ.copy()
    env["DBT_PROFILES_DIR"] = str(DBT_PROFILES_DIR)
    return env

def md_codeblock(text: str) -> str:
    text = (text or "").rstrip()
    return f"```text\n{text}\n```" if text else "```text\n(no output)\n```"

def write_report(results: List[CheckResult]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    passed = sum(1 for r in results if r.ok)
    total = len(results)

    lines: List[str] = []
    lines.append("# QA Report")
    lines.append(f"- Generated: **{now_utc_str()}**")
    lines.append(f"- Summary: **{passed}/{total} checks passed**")
    if QA_COMPILE_ONLY:
        lines.append("- Mode: **compile-only** (QA_COMPILE_ONLY=1)")
    lines.append("")
    lines.append("## Results")

    for r in results:
        status = "✅ PASS" if r.ok else "❌ FAIL"
        mand = "mandatory" if r.mandatory else "optional"
        lines.append(f"### {status} — {r.name} ({mand})")
        lines.append(md_codeblock(r.details))
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

def preflight() -> CheckResult:
    issues = []

    if not DBT_PROJECT_DIR.exists():
        issues.append(f"DBT_PROJECT_DIR not found: {DBT_PROJECT_DIR}")
    if not (DBT_PROJECT_DIR / "dbt_project.yml").exists():
        issues.append(f"dbt_project.yml not found in: {DBT_PROJECT_DIR}")

    if not DBT_PROFILES_DIR.exists():
        issues.append(f"DBT_PROFILES_DIR folder not found: {DBT_PROFILES_DIR}")
    if not (DBT_PROFILES_DIR / "profiles.yml").exists():
        issues.append(f"profiles.yml not found in: {DBT_PROFILES_DIR}")

    code, out = run_cmd([DBT_BIN, "--version"])
    if code != 0:
        issues.append("dbt --version failed:\n" + out)

    if issues:
        return CheckResult("preflight (paths + dbt version)", False, "\n".join(issues), True)

    return CheckResult(
        "preflight (paths + dbt version)",
        True,
        f"DBT_BIN={DBT_BIN}\nDBT_PROJECT_DIR={DBT_PROJECT_DIR}\nDBT_PROFILES_DIR={DBT_PROFILES_DIR}",
        True,
    )

def check_dbt_parse() -> CheckResult:
    code, out = run_cmd([DBT_BIN, "parse"], cwd=DBT_PROJECT_DIR, env=dbt_env())
    return CheckResult("dbt parse", code == 0, out, True)

def check_dbt_compile() -> CheckResult:
    code, out = run_cmd([DBT_BIN, "compile"], cwd=DBT_PROJECT_DIR, env=dbt_env())
    return CheckResult("dbt compile", code == 0, out, True)

def check_dbt_test() -> CheckResult:
    if QA_COMPILE_ONLY:
        return CheckResult(f"dbt test (select: {DBT_TEST_SELECT})", True, "Skipped (QA_COMPILE_ONLY=1)", False)

    code, out = run_cmd([DBT_BIN, "test", "--select", DBT_TEST_SELECT], cwd=DBT_PROJECT_DIR, env=dbt_env())
    return CheckResult(f"dbt test (select: {DBT_TEST_SELECT})", code == 0, out, True)

def main() -> int:
    results: List[CheckResult] = []

    results.append(preflight())
    if not results[-1].ok:
        write_report(results)
        print(f"QA report written to: {REPORT_PATH}")
        return 1

    results.append(check_dbt_parse())
    results.append(check_dbt_compile())
    results.append(check_dbt_test())

    write_report(results)
    print(f"QA report written to: {REPORT_PATH}")

    failed_mandatory = [r for r in results if r.mandatory and not r.ok]
    return 1 if failed_mandatory else 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MRT Runner (Music/Media Repair Toolkit)
- 用一個入口，依序跑多個你已有的腳本/指令
- 支援：列出步驟、挑步驟、從某步繼續、dry-run（乾跑）、log、失敗即停
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Task:
    id: str
    desc: str
    cmd: str
    cwd: Optional[str] = None
    env: Optional[Dict[str, str]] = None
    allow_fail: bool = False


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def load_tasks(tasks_path: Path) -> List[Task]:
    if not tasks_path.exists():
        raise FileNotFoundError(f"Tasks file not found: {tasks_path}")

    data = json.loads(tasks_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Tasks file must be a JSON array of task objects.")

    tasks: List[Task] = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Task #{i} must be an object.")
        tasks.append(
            Task(
                id=str(item.get("id", f"step{i+1}")),
                desc=str(item.get("desc", "")),
                cmd=str(item["cmd"]),
                cwd=item.get("cwd"),
                env=item.get("env"),
                allow_fail=bool(item.get("allow_fail", False)),
            )
        )
    return tasks


def select_tasks(tasks: List[Task], only: Optional[List[str]], start: Optional[str]) -> List[Task]:
    by_id = {t.id: t for t in tasks}

    if only:
        missing = [x for x in only if x not in by_id]
        if missing:
            raise KeyError(f"Unknown task id(s): {missing}")
        return [by_id[x] for x in only]

    if start:
        if start not in by_id:
            raise KeyError(f"Unknown start task id: {start}")
        idx = next(i for i, t in enumerate(tasks) if t.id == start)
        return tasks[idx:]

    return tasks


def format_cmd(cmd: str) -> List[str]:
    # 允許使用一行字串（含引號）描述命令
    return shlex.split(cmd, posix=os.name != "nt")


def run_one(task: Task, dry_run: bool, log_file: Optional[Path]) -> Tuple[bool, int]:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"[{ts}] ▶ {task.id} — {task.desc}".strip()
    cmdline = task.cmd

    print("\n" + header)
    print("    $", cmdline)

    if dry_run:
        print("    (dry-run) ✅ 不執行，只顯示命令")
        if log_file:
            log_file.write_text("", encoding="utf-8") if not log_file.exists() else None
            with log_file.open("a", encoding="utf-8") as f:
                f.write(header + "\n")
                f.write("    $ " + cmdline + "\n")
                f.write("    (dry-run)\n\n")
        return True, 0

    args = format_cmd(cmdline)

    env = os.environ.copy()
    if task.env:
        env.update({str(k): str(v) for k, v in task.env.items()})

    cwd = task.cwd or None

    try:
        proc = subprocess.run(
            args,
            cwd=cwd,
            env=env,
            check=False,
            text=True,
        )
        ok = (proc.returncode == 0) or task.allow_fail

        if log_file:
            log_file.write_text("", encoding="utf-8") if not log_file.exists() else None
            with log_file.open("a", encoding="utf-8") as f:
                f.write(header + "\n")
                f.write("    $ " + cmdline + "\n")
                f.write(f"    returncode={proc.returncode}\n")
                f.write("\n")

        if ok:
            print(f"    ✅ 完成 (code={proc.returncode})" + (" (allow_fail)" if task.allow_fail and proc.returncode != 0 else ""))
        else:
            print(f"    ❌ 失敗 (code={proc.returncode})")

        return ok, proc.returncode

    except FileNotFoundError as ex:
        print(f"    ❌ 命令不存在：{ex}")
        return False, 127
    except Exception as ex:
        print(f"    ❌ 執行例外：{ex}")
        return False, 1


def main():
    ap = argparse.ArgumentParser(
        prog="run-mrt.py",
        description="MRT Runner — 用任務清單依序跑你的腳本/工具（含 dry-run / log / 續跑）"
    )
    ap.add_argument("--tasks", default="mrt_tasks.json", help="任務清單 JSON 檔（預設 mrt_tasks.json）")
    ap.add_argument("--list", action="store_true", help="列出所有步驟，不執行")
    ap.add_argument("--run", action="store_true", help="執行任務（不加 --run 只會列出/檢查）")
    ap.add_argument("--only", nargs="+", help="只跑指定 task id（空白分隔）")
    ap.add_argument("--start", help="從指定 task id 開始跑（包含該步）")
    ap.add_argument("--dry-run", action="store_true", help="乾跑：只印命令不執行（dry run＝只演算不落盤）")
    ap.add_argument("--log", default=None, help="把結果附加寫入 log 檔，例如 mrt_run.log")
    ap.add_argument("--continue-on-fail", action="store_true", help="遇到失敗仍繼續（預設失敗就停止）")

    args = ap.parse_args()

    tasks_path = Path(args.tasks).resolve()
    tasks = load_tasks(tasks_path)

    if args.list or (not args.run):
        print(f"📌 Tasks file: {tasks_path}")
        print("🧾 Steps:")
        for t in tasks:
            cwd = f" (cwd={t.cwd})" if t.cwd else ""
            af = " [allow_fail]" if t.allow_fail else ""
            print(f"  - {t.id}{af}: {t.desc}{cwd}")
            print(f"      $ {t.cmd}")
        if not args.run:
            print("\nℹ️  要執行請加：--run  （可先用 --dry-run 檢查）")
        if args.list and not args.run:
            return

    chosen = select_tasks(tasks, args.only, args.start)
    log_file = Path(args.log).resolve() if args.log else None

    print(f"\n🚀 開始執行：{len(chosen)} step(s)")
    for t in chosen:
        ok, code = run_one(t, dry_run=args.dry_run, log_file=log_file)
        if not ok and not args.continue_on_fail:
            print("\n🛑 已停止：遇到失敗步驟。你可用 --start <task_id> 續跑。")
            sys.exit(code)

    print("\n🔥 全部步驟完成")


if __name__ == "__main__":
    main()

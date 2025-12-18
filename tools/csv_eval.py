from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
from datetime import datetime
import sys
import hashlib

def sniff_delimiter(sample: str) -> str:
    if sample.count("\t") > sample.count(",") and sample.count("\t") > sample.count(";"):
        return "\t"
    if sample.count(";") > sample.count(","):
        return ";"
    return ","

def stable_hash_row(row: list[str]) -> str:
    s = "\u241f".join(row)  # unit separator-ish
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="input folder containing csv files")
    ap.add_argument("--outdir", default="./work", help="where to write eval reports")
    ap.add_argument("--required", default="", help="required columns, comma-separated")
    ap.add_argument("--max-dup-scan", type=int, default=200000, help="max rows to scan for duplicates (per file)")
    args = ap.parse_args()

    inp = Path(args.inp).resolve()
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    required = [c.strip() for c in args.required.split(",") if c.strip()]

    if not inp.exists():
        print(f"Input folder not found: {inp}", file=sys.stderr)
        sys.exit(2)

    files = sorted([p for p in inp.rglob("*.csv") if p.is_file()])
    if not files:
        print("No .csv files found.", file=sys.stderr)
        sys.exit(3)

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "input_root": str(inp),
        "required_columns": required,
        "overall_status": "PASS",
        "pass_count": 0,
        "warn_count": 0,
        "fail_count": 0,
        "files": []
    }

    def bump(status: str):
        if status == "PASS":
            report["pass_count"] += 1
        elif status == "WARN":
            report["warn_count"] += 1
            report["overall_status"] = "WARN" if report["overall_status"] == "PASS" else report["overall_status"]
        else:
            report["fail_count"] += 1
            report["overall_status"] = "FAIL"

    for f in files:
        rel = str(f.relative_to(inp)).replace("\\", "/")
        item = {
            "file": rel,
            "status": "PASS",
            "encoding_used": None,
            "detected_delimiter": None,
            "rows": 0,
            "cols": 0,
            "missing_required_columns": [],
            "empty_rows": 0,
            "duplicate_rows_est": None,
            "errors": [],
            "notes": []
        }

        # read with fallback
        try:
            text = f.read_text(encoding="utf-8-sig", errors="strict")
            item["encoding_used"] = "utf-8-sig"
        except UnicodeDecodeError:
            text = f.read_text(encoding="cp950", errors="replace")
            item["encoding_used"] = "cp950(replace)"

        delim = sniff_delimiter(text[:2048])
        item["detected_delimiter"] = delim

        rows = list(csv.reader(text.splitlines(), delimiter=delim))
        if not rows:
            item["status"] = "FAIL"
            item["errors"].append("empty_file")
            bump(item["status"])
            report["files"].append(item)
            continue

        header = [h.strip() for h in rows[0]]
        item["cols"] = len(header)

        body = rows[1:]
        item["rows"] = len(body)

        # empty rows
        empty_rows = 0
        for r in body:
            if all((c.strip() == "" for c in r)):
                empty_rows += 1
        item["empty_rows"] = empty_rows
        if empty_rows > 0:
            item["status"] = "WARN"
            item["notes"].append(f"has_empty_rows={empty_rows}")

        # required columns
        missing = [c for c in required if c not in header]
        item["missing_required_columns"] = missing
        if missing:
            item["status"] = "FAIL"
            item["errors"].append(f"missing_required_columns: {missing}")

        # duplicate scan (approx)
        max_scan = min(len(body), max(0, args.max_dup_scan))
        if max_scan > 0:
            seen = set()
            dup = 0
            for r in body[:max_scan]:
                h = stable_hash_row(r)
                if h in seen:
                    dup += 1
                else:
                    seen.add(h)
            item["duplicate_rows_est"] = {"scanned": max_scan, "dups": dup}
            if dup > 0 and item["status"] != "FAIL":
                item["status"] = "WARN"
                item["notes"].append(f"duplicate_rows_est={dup} (scanned={max_scan})")

        bump(item["status"])
        report["files"].append(item)

    # write json + csv
    json_path = outdir / "mrt_eval.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    csv_path = outdir / "mrt_eval.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as fo:
        w = csv.writer(fo)
        w.writerow(["file", "status", "rows", "cols", "detected_delimiter", "encoding_used",
                    "missing_required_columns", "empty_rows", "dup_scanned", "dup_count", "notes", "errors"])
        for it in report["files"]:
            dup_scanned = ""
            dup_count = ""
            if it["duplicate_rows_est"]:
                dup_scanned = it["duplicate_rows_est"]["scanned"]
                dup_count = it["duplicate_rows_est"]["dups"]
            w.writerow([
                it["file"], it["status"], it["rows"], it["cols"],
                it["detected_delimiter"], it["encoding_used"],
                ";".join(it["missing_required_columns"]),
                it["empty_rows"], dup_scanned, dup_count,
                "|".join(it["notes"]),
                "|".join(it["errors"]),
            ])

    print(f"✅ MRT eval written:\n- {json_path}\n- {csv_path}")
    print(f"Overall: {report['overall_status']}  (PASS={report['pass_count']}, WARN={report['warn_count']}, FAIL={report['fail_count']})")

    sys.exit(0 if report["overall_status"] != "FAIL" else 6)

if __name__ == "__main__":
    main()

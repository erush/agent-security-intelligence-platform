from __future__ import annotations

import inspect
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SDK_ROOT = ROOT / "external" / "kaggle_jed"
PACKAGE_ROOT = SDK_ROOT / "aicomp_sdk"

if str(SDK_ROOT) not in sys.path:
    sys.path.insert(0, str(SDK_ROOT))


KEYWORDS = (
    "Attack",
    "Candidate",
    "Algorithm",
    "Env",
    "Result",
    "Trace",
    "Replay",
)


def iter_python_files(root: Path):
    for path in root.rglob("*.py"):
        if "__pycache__" not in path.parts:
            yield path


def module_name_from_path(path: Path) -> str:
    rel = path.relative_to(SDK_ROOT).with_suffix("")
    return ".".join(rel.parts)


def safe_import(module_name: str):
    try:
        return __import__(module_name, fromlist=["*"])
    except Exception as exc:
        return exc


def inspect_module(module_name: str, module) -> list[dict]:
    rows: list[dict] = []

    for name, obj in inspect.getmembers(module):
        if not any(k.lower() in name.lower() for k in KEYWORDS):
            continue

        if inspect.isclass(obj) or inspect.isfunction(obj):
            try:
                signature = str(inspect.signature(obj))
            except Exception:
                signature = "signature unavailable"

            try:
                source_file = inspect.getsourcefile(obj)
            except Exception:
                source_file = None

            rows.append(
                {
                    "module": module_name,
                    "name": name,
                    "type": "class" if inspect.isclass(obj) else "function",
                    "signature": signature,
                    "source_file": source_file,
                }
            )

    return rows


def print_rows(rows: list[dict]) -> None:
    print("=" * 100)
    print("SDK CONTRACT OBJECTS")
    print("=" * 100)

    for row in rows:
        print()
        print(f"{row['type'].upper()}: {row['name']}")
        print(f"module    : {row['module']}")
        print(f"signature : {row['signature']}")
        print(f"file      : {row['source_file']}")

    print()
    print("=" * 100)
    print(f"Objects found: {len(rows)}")
    print("=" * 100)


def print_attack_py_candidates(rows: list[dict]) -> None:
    print()
    print("=" * 100)
    print("LIKELY SUBMISSION CONTRACT")
    print("=" * 100)

    likely = [
        row
        for row in rows
        if (
            "Attack" in row["name"]
            or "Candidate" in row["name"]
            or "Algorithm" in row["name"]
        )
    ]

    for row in likely:
        print()
        print(f"{row['name']}")
        print(f"  module    : {row['module']}")
        print(f"  signature : {row['signature']}")


def main() -> None:
    rows: list[dict] = []

    print("=" * 100)
    print("SDK TREE")
    print("=" * 100)

    for path in iter_python_files(PACKAGE_ROOT):
        print(path.relative_to(SDK_ROOT))

    for path in iter_python_files(PACKAGE_ROOT):
        module_name = module_name_from_path(path)
        module = safe_import(module_name)

        if isinstance(module, Exception):
            continue

        rows.extend(inspect_module(module_name, module))

    rows = sorted(
        rows,
        key=lambda r: (r["module"], r["name"]),
    )

    print_rows(rows)
    print_attack_py_candidates(rows)


if __name__ == "__main__":
    main()
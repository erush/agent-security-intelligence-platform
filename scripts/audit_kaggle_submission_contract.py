from __future__ import annotations

import inspect
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SDK_ROOT = ROOT / "external" / "kaggle_jed"

if str(SDK_ROOT) not in sys.path:
    sys.path.insert(0, str(SDK_ROOT))


def show_object(name: str, obj) -> None:
    print("=" * 80)
    print(name)
    print("=" * 80)
    print(obj)
    print()

    try:
        print(inspect.signature(obj))
    except Exception as exc:
        print(f"signature unavailable: {exc}")

    print()

    try:
        print(inspect.getsource(obj))
    except Exception as exc:
        print(f"source unavailable: {exc}")

    print()


def main() -> None:
    imports = [
        ("AttackAlgorithmBase", "aicomp_sdk.attacks.base", "AttackAlgorithmBase"),
        ("AttackCandidate", "aicomp_sdk.attacks.base", "AttackCandidate"),
        ("scoring", "aicomp_sdk.scoring", None),
        ("predicates", "aicomp_sdk.core.predicates", None),
    ]

    for label, module_name, object_name in imports:
        try:
            module = __import__(module_name, fromlist=[object_name] if object_name else ["*"])
            obj = getattr(module, object_name) if object_name else module
            show_object(label, obj)
        except Exception as exc:
            print("=" * 80)
            print(label)
            print("=" * 80)
            print(f"IMPORT FAILED: {module_name}.{object_name or ''}")
            print(exc)
            print()

    attack_file = ROOT / "kaggle" / "attack.py"

    print("=" * 80)
    print("Current kaggle/attack.py")
    print("=" * 80)

    if attack_file.exists():
        print(attack_file.read_text(encoding="utf-8"))
    else:
        print("kaggle/attack.py not found")


if __name__ == "__main__":
    main()
    
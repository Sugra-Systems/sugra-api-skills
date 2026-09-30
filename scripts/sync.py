"""Copy the skills in skills/ into every vendor package. Stdlib only.

skills/ is the only place to edit a skill. Each package gets a real copy:
plugin directories reject symlinks and paths outside the package folder.

    python scripts/sync.py           write the copies
    python scripts/sync.py --check   exit 1 when a copy differs from skills/
"""

from __future__ import annotations

import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "skills"
OPENAI_ONLY = ("agents/openai.yaml",)
# package folder -> skill files (relative to a skill folder) it leaves out
PACKAGES = {
    "plugins/sugra-api": OPENAI_ONLY,
    "providers/openai/sugra-api": (),
    "providers/grok/sugra-api": OPENAI_ONLY,
}


def files_under(base: Path) -> dict[str, bytes]:
    if not base.is_dir():
        return {}
    out = {}
    for path in sorted(base.rglob("*")):
        if path.is_symlink():
            raise SystemExit(f"FAIL {path.relative_to(ROOT)}: symlink")
        if path.is_file():
            out[path.relative_to(base).as_posix()] = path.read_bytes()
    return out


def expected(excluded: tuple[str, ...]) -> dict[str, bytes]:
    out = {}
    for rel, data in files_under(SOURCE).items():
        inside_skill = PurePosixPath(*PurePosixPath(rel).parts[1:]).as_posix()
        if inside_skill not in excluded:
            out[rel] = data
    return out


def drift() -> list[str]:
    problems = []
    for package, excluded in PACKAGES.items():
        want = expected(excluded)
        have = files_under(ROOT / package / "skills")
        for rel in sorted(want.keys() | have.keys()):
            label = f"{package}/skills/{rel}"
            if rel not in have:
                problems.append(f"missing {label}")
            elif rel not in want:
                problems.append(f"extra {label}")
            elif have[rel] != want[rel]:
                problems.append(f"differs {label}")
    return problems


def write() -> None:
    for package, excluded in PACKAGES.items():
        target = ROOT / package / "skills"
        want = expected(excluded)
        have = files_under(target)
        for rel in sorted(have.keys() - want.keys()):
            (target / rel).unlink()
            print(f"removed {package}/skills/{rel}")
        for rel, data in want.items():
            if have.get(rel) != data:
                dest = target / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
                print(f"wrote {package}/skills/{rel}")
        for folder in sorted(target.rglob("*"), reverse=True):
            if folder.is_dir() and not any(folder.iterdir()):
                folder.rmdir()


def main(argv: list[str]) -> int:
    if not SOURCE.is_dir():
        print("FAIL skills/ missing", file=sys.stderr)
        return 1
    if argv[1:] == ["--check"]:
        problems = drift()
        for line in problems:
            print(f"FAIL {line}", file=sys.stderr)
        if problems:
            print("FAIL edit skills/ only, then run python scripts/sync.py", file=sys.stderr)
            return 1
        print("ok packages match skills/")
        return 0
    if argv[1:]:
        print(__doc__, file=sys.stderr)
        return 2
    write()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

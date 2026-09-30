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


def is_link(path: Path) -> bool:
    return path.is_symlink() or path.is_junction()


def guard(path: Path) -> None:
    """Refuse a path outside the repository or one reached through a link."""
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        raise SystemExit(f"FAIL {path}: outside the repository") from None
    current = ROOT
    for part in rel.parts:
        current = current / part
        if is_link(current):
            raise SystemExit(f"FAIL {current.relative_to(ROOT).as_posix()}: symlink")
    if path.exists() and not path.resolve().is_relative_to(ROOT):
        raise SystemExit(f"FAIL {rel.as_posix()}: resolves outside the repository")


def files_under(base: Path) -> dict[str, bytes]:
    guard(base)
    if not base.is_dir():
        return {}
    out = {}
    for path in sorted(base.rglob("*")):
        if is_link(path):
            raise SystemExit(f"FAIL {path.relative_to(ROOT).as_posix()}: symlink")
        if path.is_file():
            out[path.relative_to(base).as_posix()] = path.read_bytes()
    return out


def keep(rel: str, excluded: tuple[str, ...]) -> bool:
    """rel is skill/path; excluded names paths inside a skill folder."""
    return PurePosixPath(*PurePosixPath(rel).parts[1:]).as_posix() not in excluded


def expected(excluded: tuple[str, ...]) -> dict[str, bytes]:
    return {rel: data for rel, data in files_under(SOURCE).items() if keep(rel, excluded)}


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
            dest = target / rel
            guard(dest)
            dest.unlink()
            print(f"removed {package}/skills/{rel}")
        for rel, data in want.items():
            if have.get(rel) != data:
                dest = target / rel
                guard(dest.parent)
                dest.parent.mkdir(parents=True, exist_ok=True)
                guard(dest)
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

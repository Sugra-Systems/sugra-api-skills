"""Build the OpenAI Plugins Directory ZIP from providers/openai/sugra-api. Stdlib only.

    python scripts/build_openai_zip.py                 package with mcp.json
    python scripts/build_openai_zip.py --skills-only   package without mcp.json

The ZIP is built from a clean commit and names that commit in its file name and
in the archive comment, so every uploaded version can be traced to its source.
The same commit always gives the same bytes.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

import sync

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "providers" / "openai" / "sugra-api"
DIST = ROOT / "dist"
LISTING_FIELD_LIMIT = 30


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def main(argv: list[str]) -> int:
    flags = set(argv[1:])
    unknown = flags - {"--skills-only", "--allow-dirty"}
    if unknown:
        print(__doc__, file=sys.stderr)
        return 2
    problems = sync.drift()
    if problems:
        for line in problems:
            print(f"FAIL {line}", file=sys.stderr)
        return 1
    dirty = git("status", "--porcelain", "--", "skills", "providers/openai")
    if dirty and "--allow-dirty" not in flags:
        print("FAIL commit skills/ and providers/openai first:\n" + dirty, file=sys.stderr)
        return 1
    commit = git("rev-parse", "HEAD") + ("-dirty" if dirty else "")

    manifest = json.loads((PACKAGE / "plugin.json").read_text(encoding="utf-8"))
    interface = manifest["extensions"]["com.openai"]["interface"]
    for field in ("displayName", "shortDescription"):
        if len(interface[field]) > LISTING_FIELD_LIMIT:
            print(f"note: {field} is {len(interface[field])} chars, the directory form allows {LISTING_FIELD_LIMIT}")

    skills_only = "--skills-only" in flags
    files = []
    for path in sorted(PACKAGE.rglob("*")):
        if path.is_symlink():
            print(f"FAIL {path.relative_to(ROOT)}: symlink", file=sys.stderr)
            return 1
        if not path.is_file():
            continue
        rel = path.relative_to(PACKAGE).as_posix()
        if skills_only and rel == "mcp.json":
            continue
        files.append((rel, path.read_bytes()))

    suffix = "-skills-only" if skills_only else ""
    DIST.mkdir(exist_ok=True)
    out = DIST / f"sugra-api-openai-{manifest['version']}{suffix}-{commit[:12]}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.comment = f"Sugra-Systems/sugra-api-skills {commit} providers/openai/sugra-api".encode()
        for rel, data in files:
            info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    print(f"{out.relative_to(ROOT).as_posix()}")
    print(f"version {manifest['version']} commit {commit} files {len(files)} sha256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

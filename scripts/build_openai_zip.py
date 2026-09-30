"""Build the OpenAI Plugins Directory ZIP from providers/openai/sugra-api. Stdlib only.

    python scripts/build_openai_zip.py                 package with mcp.json
    python scripts/build_openai_zip.py --skills-only   package without mcp.json

The ZIP holds the files committed at HEAD, never the working tree. The builder
refuses while skills/ or providers/openai/ differ from HEAD (untracked files
included) and while the package copy of the skills differs from skills/ at HEAD.
It names the commit in the file name and in the archive comment. Entries are
stored uncompressed with a fixed date, mode and host, so one commit gives one
ZIP, byte for byte.
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
PACKAGE = "providers/openai/sugra-api"
DIST = ROOT / "dist"
LISTING_FIELDS = ("displayName", "shortDescription")
LISTING_FIELD_NOTE = 30


def git(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True).stdout


def tree(prefix: str) -> dict[str, str]:
    """Regular files under prefix at HEAD: path relative to prefix -> blob id."""
    out = {}
    for entry in git("ls-tree", "-r", "-z", "--full-tree", "HEAD", "--", prefix).split(b"\0"):
        if not entry:
            continue
        meta, raw = entry.split(b"\t", 1)
        mode, kind, blob = meta.decode().split()
        path = raw.decode("utf-8")
        if kind != "blob" or mode not in ("100644", "100755"):
            raise SystemExit(f"FAIL {path}: mode {mode} is not a regular file")
        out[path[len(prefix) + 1 :]] = blob
    return out


def main(argv: list[str]) -> int:
    flags = set(argv[1:])
    if flags - {"--skills-only"}:
        print(__doc__, file=sys.stderr)
        return 2
    dirty = git("status", "--porcelain", "--untracked-files=all", "--", "skills", "providers/openai")
    if dirty:
        print("FAIL commit skills/ and providers/openai first:\n" + dirty.decode(), file=sys.stderr)
        return 1
    commit = git("rev-parse", "HEAD").decode().strip()

    package = tree(PACKAGE)
    excluded = sync.PACKAGES[PACKAGE]
    want = {rel: blob for rel, blob in tree("skills").items() if sync.keep(rel, excluded)}
    have = {rel[len("skills/") :]: blob for rel, blob in package.items() if rel.startswith("skills/")}
    if want != have:
        for rel in sorted(want.keys() | have.keys()):
            if want.get(rel) != have.get(rel):
                print(f"FAIL {PACKAGE}/skills/{rel} differs from skills/ at HEAD", file=sys.stderr)
        print("FAIL run python scripts/sync.py and commit", file=sys.stderr)
        return 1

    manifest = json.loads(git("cat-file", "blob", package["plugin.json"]))
    interface = manifest.get("extensions", {}).get("com.openai", {}).get("interface", {})
    for field in LISTING_FIELDS:
        value = interface.get(field)
        if not isinstance(value, str) or not value.strip():
            print(f"FAIL plugin.json interface.{field} must be a non-empty string", file=sys.stderr)
            return 1
        if len(value) > LISTING_FIELD_NOTE:
            print(f"note: {field} is {len(value)} chars; the directory docs name {LISTING_FIELD_NOTE}")

    skills_only = "--skills-only" in flags
    names = sorted(rel for rel in package if not (skills_only and rel == "mcp.json"))
    suffix = "-skills-only" if skills_only else ""
    DIST.mkdir(exist_ok=True)
    out = DIST / f"sugra-api-openai-{manifest['version']}{suffix}-{commit[:12]}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_STORED) as archive:
        archive.comment = f"Sugra-Systems/sugra-api-skills {commit} {PACKAGE}".encode()
        for rel in names:
            info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, git("cat-file", "blob", package[rel]))
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    print(out.relative_to(ROOT).as_posix())
    print(f"version {manifest['version']} commit {commit} files {len(names)} sha256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

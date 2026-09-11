"""Stdlib checks for the Sugra API skill pack. No third-party deps."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "sugra-api"
SKILLS = PLUGIN / "skills"
EXPECTED = (
    "using-sugra-api",
    "live-docs",
    "connect",
    "auth-and-quota",
    "discover-and-call",
    "envelope-and-attribution",
    "cross-domain-briefing",
)
FRONTMATTER_RE = re.compile(
    r"^---\nname: (?P<name>[^\n]+)\ndescription: (?P<description>.+)\n---\n",
    re.DOTALL,
)
TIER_C = (
    "yahoo",
    "finnhub",
    "coingecko",
    "tomorrow.io",
    "alpha vantage",
    "polygon",
    "tiingo",
    "cboe",
)
BANS = ("real-time", "realtime", "financial intelligence", "blackbox")


def fail(msg: str) -> None:
    print(f"FAIL {msg}", file=sys.stderr)
    raise SystemExit(1)


def copy_lint(text: str, label: str) -> None:
    if not text.isascii():
        fail(f"{label}: must be plain ASCII")
    if "\u2014" in text or "—" in text:
        fail(f"{label}: em dash")
    lowered = text.lower()
    for ban in BANS:
        if ban in lowered:
            fail(f"{label}: banned phrase {ban}")
    for fragment in TIER_C:
        if fragment in lowered:
            fail(f"{label}: commercial name {fragment}")


def main() -> None:
    slugs = sorted(p.name for p in SKILLS.iterdir() if p.is_dir())
    if tuple(slugs) != tuple(sorted(EXPECTED)):
        fail(f"skill folders {slugs} != {EXPECTED}")

    for slug in EXPECTED:
        path = SKILLS / slug / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            fail(f"{slug}: missing YAML name/description frontmatter")
        if match.group("name") != slug:
            fail(f"{slug}: frontmatter name {match.group('name')!r}")
        if len(match.group("description").strip()) < 40:
            fail(f"{slug}: description too short")
        copy_lint(text, str(path.relative_to(ROOT)))

    using = (SKILLS / "using-sugra-api" / "SKILL.md").read_text(encoding="utf-8")
    if "x-api-key" not in using or "https://sugra.ai" not in using:
        fail("using-sugra-api must teach HTTPS and x-api-key")
    if "mcp.sugra.ai" not in using:
        fail("using-sugra-api must teach hosted MCP")

    docs = (SKILLS / "live-docs" / "SKILL.md").read_text(encoding="utf-8")
    for needle in ("/openapi.json", "/sources", "/stats", "tools/list"):
        if needle not in docs:
            fail(f"live-docs must mention {needle}")

    connect = (SKILLS / "connect" / "SKILL.md").read_text(encoding="utf-8")
    for needle in ("x-api-key", "mcp.sugra.ai", "sugra-api-mcp", "Claude Desktop", "ChatGPT"):
        if needle not in connect:
            fail(f"connect must mention {needle}")

    discover = (SKILLS / "discover-and-call" / "SKILL.md").read_text(encoding="utf-8")
    if "/openapi.json" not in discover:
        fail("discover-and-call must point at live OpenAPI")
    if "search_endpoints" not in discover or "call_endpoint" not in discover:
        fail("discover-and-call must teach the MCP loop")

    plugin = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    claude = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    grok = json.loads((ROOT / ".grok-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    if plugin["name"] != "sugra-api":
        fail("plugin.json name")
    if claude["name"] != "sugra-api-skills" or grok["name"] != "sugra-api-skills":
        fail("marketplace name")
    if claude["plugins"][0]["source"] != "./plugins/sugra-api":
        fail("claude marketplace source")
    grok_path = grok["plugins"][0]["source"]["path"]
    if grok_path != "./plugins/sugra-api":
        fail("grok marketplace source")
    copy_lint(json.dumps(plugin), "plugin.json")
    copy_lint(json.dumps(claude), "claude marketplace.json")
    copy_lint(json.dumps(grok), "grok marketplace.json")
    print("ok", len(EXPECTED), "skills")


if __name__ == "__main__":
    main()

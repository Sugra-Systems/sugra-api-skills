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
    "auth-and-quota",
    "connect",
    "cross-domain-briefing",
    "discover-and-call",
    "envelope-and-attribution",
    "live-docs",
    "using-sugra-api",
)
FRONTMATTER_RE = re.compile(
    r"^---\n"
    r"name: (?P<name>[^\n]+)\n"
    r"description: (?P<description>.+)\n"
    r"license: MIT\n"
    r"metadata:\n"
    r"  author: Sugra Systems, Inc.\n"
    r"---\n",
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
DIRECTIONS = (
    "Sugra Finance",
    "Sugra Macro",
    "Sugra Entity",
    "Sugra Net Atlas",
    "Sugra News",
    "Sugra Earth",
    "Sugra Research",
)


def fail(msg: str) -> None:
    print(f"FAIL {msg}", file=sys.stderr)
    raise SystemExit(1)


def copy_lint(text: str, label: str) -> None:
    if not text.isascii():
        fail(f"{label}: must be plain ASCII")
    if "\u2014" in text:
        fail(f"{label}: em dash")
    lowered = text.lower()
    for ban in BANS:
        if ban in lowered:
            fail(f"{label}: banned phrase {ban}")
    for fragment in TIER_C:
        if fragment in lowered:
            fail(f"{label}: commercial name {fragment}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    slugs = sorted(p.name for p in SKILLS.iterdir() if p.is_dir())
    if tuple(slugs) != EXPECTED:
        fail(f"skill folders {slugs} != {EXPECTED}")

    for slug in EXPECTED:
        path = SKILLS / slug / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            fail(f"{slug}: frontmatter must be name, description, license MIT, metadata.author")
        if match.group("name") != slug:
            fail(f"{slug}: frontmatter name {match.group('name')!r}")
        description = match.group("description").strip()
        if "\n" in description:
            fail(f"{slug}: description must be one line")
        if len(description) > 500:
            fail(f"{slug}: description {len(description)} chars > 500")
        if len(description) < 40:
            fail(f"{slug}: description too short")
        if description[0].isupper() is False:
            fail(f"{slug}: description should start in third-person / imperative English")
        copy_lint(text, str(path.relative_to(ROOT)))
        line_count = text.count("\n") + 1
        if line_count > 500:
            fail(f"{slug}: SKILL.md {line_count} lines > 500")

    using = (SKILLS / "using-sugra-api" / "SKILL.md").read_text(encoding="utf-8")
    for needle in ("x-api-key", "https://sugra.ai", "mcp.sugra.ai", "docs.sugra.ai"):
        if needle not in using:
            fail(f"using-sugra-api must mention {needle}")
    for direction in DIRECTIONS:
        if direction not in using:
            fail(f"using-sugra-api must name {direction}")

    docs = (SKILLS / "live-docs" / "SKILL.md").read_text(encoding="utf-8")
    for needle in ("https://docs.sugra.ai", "Ask AI", "/openapi.json", "/sources", "/stats", "sugra.systems/blog"):
        if needle not in docs:
            fail(f"live-docs must mention {needle}")

    connect = (SKILLS / "connect" / "SKILL.md").read_text(encoding="utf-8")
    for needle in ("x-api-key", "mcp.sugra.ai", "sugra-api-mcp", "ChatGPT"):
        if needle not in connect:
            fail(f"connect must mention {needle}")
    clients = SKILLS / "connect" / "references" / "clients.md"
    if not clients.is_file():
        fail("connect/references/clients.md missing")
    copy_lint(clients.read_text(encoding="utf-8"), "connect/references/clients.md")

    discover = (SKILLS / "discover-and-call" / "SKILL.md").read_text(encoding="utf-8")
    if "docs.sugra.ai" not in discover or "/openapi.json" not in discover:
        fail("discover-and-call must use docs.sugra.ai and OpenAPI")
    if "search_endpoints" not in discover or "call_endpoint" not in discover:
        fail("discover-and-call must teach the MCP loop")

    claude_plugin = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
    codex_plugin = load_json(PLUGIN / ".codex-plugin" / "plugin.json")
    claude_mkt = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    grok_mkt = load_json(ROOT / ".grok-plugin" / "marketplace.json")
    agents_mkt = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    if claude_plugin["name"] != "sugra-api" or codex_plugin["name"] != "sugra-api":
        fail("plugin name")
    if claude_plugin.get("version") != "1.0.0" or codex_plugin.get("version") != "1.0.0":
        fail("plugin version")
    if claude_plugin.get("homepage") != "https://docs.sugra.ai":
        fail("plugin homepage must be docs.sugra.ai")
    if claude_plugin.get("skills") not in ("./skills", "./skills/"):
        fail("claude plugin skills path")
    if "user's language" not in using:
        fail("using-sugra-api must tell the agent to match the user's language")
    if claude_plugin["author"]["name"] != "Sugra Systems, Inc.":
        fail("plugin author")
    if claude_mkt["name"] != "sugra-api-skills" or grok_mkt["name"] != "sugra-api-skills":
        fail("marketplace name")
    if claude_mkt["plugins"][0]["source"] != "./plugins/sugra-api":
        fail("claude marketplace source")
    if grok_mkt["plugins"][0]["source"]["path"] != "./plugins/sugra-api":
        fail("grok marketplace source")
    if agents_mkt["plugins"][0]["source"]["path"] != "./plugins/sugra-api":
        fail("codex marketplace source")
    for label, obj in (
        ("plugin.json", claude_plugin),
        ("codex plugin.json", codex_plugin),
        ("claude marketplace.json", claude_mkt),
        ("grok marketplace.json", grok_mkt),
    ):
        copy_lint(json.dumps(obj), label)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    copy_lint(readme, "README.md")
    copy_lint(security, "SECURITY.md")
    copy_lint(llms, "llms.txt")
    if "docs.sugra.ai" not in readme:
        fail("README must point at docs.sugra.ai")
    if "Sugra-Systems/sugra-api-skills" not in readme:
        fail("README must name the public GitHub path")
    if "Not on GitHub yet" in readme:
        fail("README still says the pack is unpublished")
    print("ok", len(EXPECTED), "skills")


if __name__ == "__main__":
    main()

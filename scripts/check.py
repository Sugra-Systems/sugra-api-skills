"""Stdlib checks for the Sugra API skill pack. No third-party deps."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# The skill folders at the repository root are the source. plugins/sugra-api is
# the Claude package an open directory submission is bound to; it stays as it
# is until that submission closes, and its copy of the skills is checked as-is.
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
# A tool count goes stale the day the server changes; name the tools instead.
# A number, up to two qualifier words, then "tool" or "tools" - but not "tool
# call", which counts calls, not tools.
UNITS = "one|two|three|four|five|six|seven|eight|nine"
TEENS = "ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen"
TENS = "twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety"
NUMBER = rf"(?:\d+|(?:{TENS})(?:[- ](?:{UNITS}))?|{TEENS}|{UNITS})"
TOOL_COUNT_RE = re.compile(
    rf"\b{NUMBER}\s+(?:(?!of\b)[a-z-]+\s+){{0,2}}tools?\b(?!\s+calls?\b)",
    re.IGNORECASE,
)
TOOL_COUNT_HITS = (
    "one tool",
    "11 tools",
    "thirteen tools",
    "twenty-one tools",
    "three hosted gateway tools",
    "two composed tools",
)
TOOL_COUNT_MISSES = (
    "one tool call",
    "two tool calls",
    "two gateway transports",
    "the gateway tools",
    "a tool",
    "one of the tools",
)
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


def check_skills(base: Path, source: bool) -> None:
    """Check one set of the seven skills.

    source=True is the repository root: no vendor files (agents/openai.yaml
    belongs to the OpenAI package in sugra-api-plugins) and no tool counts.
    source=False is the frozen copy in plugins/sugra-api, checked as it ships.
    """
    for slug in EXPECTED:
        path = base / slug / "SKILL.md"
        if not path.is_file():
            fail(f"{path.relative_to(ROOT)} missing")
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            fail(f"{slug}: frontmatter must be name, description, license MIT")
        if "metadata:" in text.split("---", 2)[1]:
            fail(f"{slug}: put skill interface in agents/openai.yaml, not SKILL.md metadata")
        yaml_path = base / slug / "agents" / "openai.yaml"
        if source:
            if (base / slug / "agents").exists():
                fail(f"{slug}: vendor files (agents/) belong in sugra-api-plugins, not the skill source")
            for md in sorted((base / slug).rglob("*.md")):
                counted = TOOL_COUNT_RE.search(md.read_text(encoding="utf-8"))
                if counted:
                    fail(f"{md.relative_to(ROOT)}: tool count {counted.group(0)!r}; name the tools instead")
        else:
            if not yaml_path.is_file():
                fail(f"{slug}: missing agents/openai.yaml")
            yaml_text = yaml_path.read_text(encoding="utf-8")
            if "interface:" not in yaml_text or "display_name:" not in yaml_text:
                fail(f"{slug}: agents/openai.yaml must declare interface.display_name")
            copy_lint(yaml_text, str(yaml_path.relative_to(ROOT)))
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

    using = (base / "using-sugra-api" / "SKILL.md").read_text(encoding="utf-8")
    for needle in ("x-api-key", "https://sugra.ai", "mcp.sugra.ai", "docs.sugra.ai"):
        if needle not in using:
            fail(f"using-sugra-api must mention {needle}")
    for direction in DIRECTIONS:
        if direction not in using:
            fail(f"using-sugra-api must name {direction}")

    docs = (base / "live-docs" / "SKILL.md").read_text(encoding="utf-8")
    for needle in ("https://docs.sugra.ai", "Ask AI", "/openapi.json", "/sources", "/stats", "sugra.systems/blog"):
        if needle not in docs:
            fail(f"live-docs must mention {needle}")

    connect = (base / "connect" / "SKILL.md").read_text(encoding="utf-8")
    for needle in ("x-api-key", "mcp.sugra.ai", "sugra-api-mcp", "ChatGPT"):
        if needle not in connect:
            fail(f"connect must mention {needle}")
    clients = base / "connect" / "references" / "clients.md"
    if not clients.is_file():
        fail("connect/references/clients.md missing")
    copy_lint(clients.read_text(encoding="utf-8"), "connect/references/clients.md")

    discover = (base / "discover-and-call" / "SKILL.md").read_text(encoding="utf-8")
    if "docs.sugra.ai" not in discover or "/openapi.json" not in discover:
        fail("discover-and-call must use docs.sugra.ai and OpenAPI")
    if "search_endpoints" not in discover or "call_endpoint" not in discover:
        fail("discover-and-call must teach the MCP loop")
    if "user's language" not in using:
        fail("using-sugra-api must tell the agent to match the user's language")


def check_tool_count_rule() -> None:
    for text in TOOL_COUNT_HITS:
        if not TOOL_COUNT_RE.search(text):
            fail(f"tool count rule misses {text!r}")
    for text in TOOL_COUNT_MISSES:
        if TOOL_COUNT_RE.search(text):
            fail(f"tool count rule wrongly matches {text!r}")


def main() -> None:
    check_tool_count_rule()
    roots = sorted(p.parent.name for p in ROOT.glob("*/SKILL.md"))
    if tuple(roots) != EXPECTED:
        fail(f"root skill folders {roots} != {EXPECTED}")
    check_skills(ROOT, source=True)

    slugs = sorted(p.name for p in SKILLS.iterdir() if p.is_dir())
    if tuple(slugs) != EXPECTED:
        fail(f"skill folders {slugs} != {EXPECTED}")
    check_skills(SKILLS, source=False)

    portable = load_json(PLUGIN / "plugin.json")
    claude_plugin = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
    claude_mkt = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    grok_mkt = load_json(ROOT / ".grok-plugin" / "marketplace.json")
    agents_mkt = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    if (PLUGIN / ".codex-plugin").exists():
        fail("portable plugin.json with extensions.com.openai replaces .codex-plugin")
    if portable.get("name") != "sugra-api" or claude_plugin["name"] != "sugra-api":
        fail("plugin name")
    if portable.get("version") != "1.1.0" or claude_plugin.get("version") != "1.1.0":
        fail("plugin version")
    mcp_conf = load_json(PLUGIN / ".mcp.json")
    sugra_mcp = ((mcp_conf.get("mcpServers") or {}).get("sugra-api") or {})
    if sugra_mcp.get("type") != "http":
        fail(".mcp.json sugra-api must set type http")
    if sugra_mcp.get("url") != "https://app.sugra.ai/mcp":
        fail(".mcp.json must use https://app.sugra.ai/mcp (same origin as the OpenAI MCP listing)")
    if portable.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        fail("portable plugin.json must declare Agent Plugins schema")
    if "skills" in portable:
        fail("portable plugin.json must not declare skills; skills/ is discovered")
    openai_iface = ((portable.get("extensions") or {}).get("com.openai") or {}).get("interface") or {}
    if openai_iface.get("composerIcon") != "./assets/logo.png" or openai_iface.get("logo") != "./assets/logo.png":
        fail("portable extensions.com.openai interface icons")
    if claude_plugin.get("homepage") != "https://docs.sugra.ai":
        fail("plugin homepage must be docs.sugra.ai")
    if claude_plugin.get("skills") not in ("./skills", "./skills/"):
        fail("claude plugin skills path")
    logo = PLUGIN / "assets" / "logo.png"
    if not logo.is_file():
        fail("plugin assets/logo.png missing")
    policy = agents_mkt["plugins"][0].get("policy") or {}
    if policy.get("installation") != "AVAILABLE" or policy.get("authentication") != "ON_INSTALL":
        fail("codex marketplace plugin policy")
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
        ("portable plugin.json", portable),
        ("plugin.json", claude_plugin),
        ("claude marketplace.json", claude_mkt),
        ("grok marketplace.json", grok_mkt),
        ("codex marketplace.json", agents_mkt),
    ):
        copy_lint(json.dumps(obj), label)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    plugin_readme = (PLUGIN / "README.md").read_text(encoding="utf-8")
    copy_lint(plugin_readme, "plugins/sugra-api/README.md")
    copy_lint(readme, "README.md")
    copy_lint(security, "SECURITY.md")
    copy_lint(llms, "llms.txt")
    if "docs.sugra.ai" not in readme:
        fail("README must point at docs.sugra.ai")
    if "Sugra-Systems/sugra-api-skills" not in readme:
        fail("README must name the public GitHub path")
    if "chatgpt.com/plugins/plugins_6aa4f7db79848191a81e4048990545ef" not in readme:
        fail("README must link the ChatGPT Plugins Directory listing")
    if "Not on GitHub yet" in readme:
        fail("README still says the pack is unpublished")
    for client in ("Claude", "Grok", "Codex", "Cursor", "Gemini", "ChatGPT"):
        if client not in readme:
            fail(f"README must name {client}")
    if "pip install sugra-api-mcp" not in readme:
        fail("README must show pip install sugra-api-mcp")
    if "1.1.0" not in readme:
        fail("README must show pack version 1.1.0")
    if ".mcp.json" not in plugin_readme:
        fail("plugin README must mention .mcp.json")
    if "OpenAI directory zip" not in plugin_readme:
        fail("plugin README must say the OpenAI zip omits .mcp.json")
    if "LLM-ready envelope" not in readme:
        fail("README must state the product pitch")
    print("ok", len(EXPECTED), "skills")


if __name__ == "__main__":
    main()

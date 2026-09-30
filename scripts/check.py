"""Stdlib checks for the Sugra API skill pack. No third-party deps."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import sync

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
CLAUDE = ROOT / "plugins" / "sugra-api"
OPENAI = ROOT / "providers" / "openai" / "sugra-api"
GROK = ROOT / "providers" / "grok" / "sugra-api"
# each package releases on its own; bump only the package that changed
VERSIONS = {"claude": "1.2.0", "openai": "1.2.0", "grok": "1.2.0"}
MCP_URL = "https://app.sugra.ai/mcp"
AGENT_PLUGINS = "https://agent-plugins.org/schemas/1.0.0/"
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


def check_mcp(conf: dict, kind: str, label: str) -> None:
    servers = conf.get("mcpServers") or {}
    if list(servers) != ["sugra-api"] or servers["sugra-api"] != {"type": kind, "url": MCP_URL}:
        fail(f"{label} must define only sugra-api as type {kind} at {MCP_URL}")


def main() -> None:
    slugs = sorted(p.name for p in SKILLS.iterdir() if p.is_dir())
    if tuple(slugs) != EXPECTED:
        fail(f"skill folders {slugs} != {EXPECTED}")

    for slug in EXPECTED:
        path = SKILLS / slug / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            fail(f"{slug}: frontmatter must be name, description, license MIT")
        if "metadata:" in text.split("---", 2)[1]:
            fail(f"{slug}: put skill interface in agents/openai.yaml, not SKILL.md metadata")
        yaml_path = SKILLS / slug / "agents" / "openai.yaml"
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

    if "user's language" not in using:
        fail("using-sugra-api must tell the agent to match the user's language")

    problems = sync.drift()
    if problems:
        fail(f"package skills differ from skills/ ({problems[0]}); run python scripts/sync.py")

    # Claude package. The Anthropic directory submission is bound to this folder
    # and reviews every change in it, so it holds Claude files only.
    claude_plugin = load_json(CLAUDE / ".claude-plugin" / "plugin.json")
    if claude_plugin.get("name") != "sugra-api" or claude_plugin.get("version") != VERSIONS["claude"]:
        fail("claude plugin name or version")
    if claude_plugin.get("homepage") != "https://docs.sugra.ai":
        fail("claude plugin homepage must be docs.sugra.ai")
    if claude_plugin.get("privacyPolicyUrl") != "https://sugra.systems/privacy-policy":
        fail("claude plugin privacyPolicyUrl")
    if claude_plugin.get("skills") not in ("./skills", "./skills/"):
        fail("claude plugin skills path")
    if claude_plugin["author"]["name"] != "Sugra Systems, Inc.":
        fail("claude plugin author")
    for stray in ("plugin.json", "mcp.json", ".codex-plugin", ".grok-plugin", ".cursor-plugin"):
        if (CLAUDE / stray).exists():
            fail(f"plugins/sugra-api/{stray}: other vendors' files belong in providers/")
    check_mcp(load_json(CLAUDE / ".mcp.json"), "http", "plugins/sugra-api/.mcp.json")

    # OpenAI package: Agent Plugins 1.0.0, read by Codex and zipped for the Plugins Directory.
    portable = load_json(OPENAI / "plugin.json")
    if portable.get("$schema") != AGENT_PLUGINS + "plugin.schema.json":
        fail("openai plugin.json must declare the Agent Plugins schema")
    if portable.get("name") != "sugra-api" or portable.get("version") != VERSIONS["openai"]:
        fail("openai plugin name or version")
    if "skills" in portable:
        fail("openai plugin.json must not declare skills; skills/ is discovered")
    openai_iface = ((portable.get("extensions") or {}).get("com.openai") or {}).get("interface") or {}
    if openai_iface.get("composerIcon") != "./assets/logo.png" or openai_iface.get("logo") != "./assets/logo.png":
        fail("openai extensions.com.openai interface icons")
    if not (OPENAI / "assets" / "logo.png").is_file():
        fail("providers/openai/sugra-api/assets/logo.png missing")
    for stray in (".claude-plugin", ".codex-plugin", ".mcp.json", "hooks", ".app.json"):
        if (OPENAI / stray).exists():
            fail(f"providers/openai/sugra-api/{stray}: not part of the OpenAI package")
    openai_mcp = load_json(OPENAI / "mcp.json")
    if set(openai_mcp) != {"$schema", "mcpServers"} or openai_mcp["$schema"] != AGENT_PLUGINS + "mcp.schema.json":
        fail("openai mcp.json must hold only the Agent Plugins $schema and mcpServers")
    check_mcp(openai_mcp, "streamable-http", "providers/openai/sugra-api/mcp.json")

    # Grok package. Grok reads a root plugin.json before .grok-plugin/plugin.json,
    # so this folder must not carry one.
    grok_plugin = load_json(GROK / ".grok-plugin" / "plugin.json")
    if grok_plugin.get("name") != "sugra-api" or grok_plugin.get("version") != VERSIONS["grok"]:
        fail("grok plugin name or version")
    for stray in ("plugin.json", "mcp.json", ".claude-plugin", ".codex-plugin"):
        if (GROK / stray).exists():
            fail(f"providers/grok/sugra-api/{stray}: Grok would read it first or it belongs elsewhere")
    check_mcp(load_json(GROK / ".mcp.json"), "http", "providers/grok/sugra-api/.mcp.json")

    claude_mkt = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    grok_mkt = load_json(ROOT / ".grok-plugin" / "marketplace.json")
    agents_mkt = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    for label, mkt in (("claude", claude_mkt), ("grok", grok_mkt), ("codex", agents_mkt)):
        if mkt["name"] != "sugra-api-skills" or [p["name"] for p in mkt["plugins"]] != ["sugra-api"]:
            fail(f"{label} marketplace must list plugin sugra-api as sugra-api-skills")
    if claude_mkt["plugins"][0]["source"] != "./plugins/sugra-api":
        fail("claude marketplace source")
    if claude_mkt["plugins"][0].get("version") != VERSIONS["claude"]:
        fail("claude marketplace version")
    if grok_mkt["plugins"][0]["source"] != {"type": "local", "path": "./providers/grok/sugra-api"}:
        fail("grok marketplace source")
    if grok_mkt["plugins"][0].get("version") != VERSIONS["grok"]:
        fail("grok marketplace version")
    if agents_mkt["plugins"][0]["source"] != {"source": "local", "path": "./providers/openai/sugra-api"}:
        fail("codex marketplace source")
    policy = agents_mkt["plugins"][0].get("policy") or {}
    if policy.get("installation") != "AVAILABLE" or policy.get("authentication") != "ON_INSTALL":
        fail("codex marketplace plugin policy")
    for label, obj in (
        ("openai plugin.json", portable),
        ("claude plugin.json", claude_plugin),
        ("grok plugin.json", grok_plugin),
        ("claude marketplace.json", claude_mkt),
        ("grok marketplace.json", grok_mkt),
        ("codex marketplace.json", agents_mkt),
    ):
        copy_lint(json.dumps(obj), label)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    for package in (CLAUDE, OPENAI, GROK):
        package_readme = (package / "README.md").read_text(encoding="utf-8")
        label = (package / "README.md").relative_to(ROOT).as_posix()
        copy_lint(package_readme, label)
        if "scripts/sync.py" not in package_readme or MCP_URL not in package_readme:
            fail(f"{label} must name scripts/sync.py and {MCP_URL}")
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
    if "badge/version-" in readme:
        fail("README must not carry one pack version; each package versions on its own")
    if "plugins/sugra-api/skills" in readme or "plugins/sugra-api/skills" in llms:
        fail("README and llms.txt must point at skills/, the source folder")
    for text, label in ((readme, "README"), (llms, "llms.txt")):
        if "sugra.ai/stats" in text or "`/stats`" in text:
            fail(f"{label} must not point readers at /stats")
    if "LLM-ready envelope" not in readme:
        fail("README must state the product pitch")
    print("ok", len(EXPECTED), "skills")


if __name__ == "__main__":
    main()

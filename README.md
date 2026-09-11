# sugra-api-skills

Official Sugra API skills for agents.

Sugra API is intelligence infrastructure: 1,500+ endpoints across 160+ primary sources and 36 domains. An agent works it over HTTPS, over MCP, or both. This repository is the skill marketplace. It is not the MCP server (`sugra-api-mcp`) and not the HTTP cookbook (`sugra-api-cookbook`).

**Not on GitHub yet.** Local draft. Do not `/plugin marketplace add` a GitHub path until this repo is published.

## What the plugin teaches

Plugin name: `sugra-api`. Seven skills. HTTP and MCP are both complete paths.

| Skill | When |
|---|---|
| `using-sugra-api` | start here: two surfaces, skill map |
| `live-docs` | live OpenAPI, `/sources`, `/stats`, MCP `tools/list`, human docs |
| `connect` | HTTPS, hosted MCP, stdio, self-host, each client |
| `auth-and-quota` | `x-api-key`, Bearer, OAuth, plans, 401/429 |
| `discover-and-call` | find and call an operation on HTTP or MCP |
| `envelope-and-attribution` | `{data, meta}`, sources, clocks, MCP shaping |
| `cross-domain-briefing` | two or three domains in one answer |

HTTPS:

```
GET https://sugra.ai/api/v1/etf/sectors/relative-strength?window=1m
x-api-key: sugra_...
```

MCP hosted: `https://mcp.sugra.ai/mcp` (alias `https://app.sugra.ai/mcp`). Local: `pip install sugra-api-mcp`.

Free key: [app.sugra.ai/settings/billing](https://app.sugra.ai/settings/billing) (50 req/day).

Live catalog: [sugra.ai/openapi.json](https://sugra.ai/openapi.json). Do not trust this README for endpoint counts.

## Install (after GitHub publish)

Intended remote: `Sugra-Systems/sugra-api-skills`.

Claude Code:

```
/plugin marketplace add Sugra-Systems/sugra-api-skills
/plugin install sugra-api@sugra-api-skills
```

Grok (from this folder today; from GitHub after publish):

```bash
grok plugin marketplace add C:\DEV-SUGRA\sugra-api-skills
grok plugin install sugra-api --trust
```

Codex: copy each folder under `plugins/sugra-api/skills/` into `$HOME/.agents/skills/<slug>/` or `~/.codex/skills/<slug>/`.

Cursor: copy into `.cursor/skills/` or `~/.cursor/skills/`.

ChatGPT does not load SKILL.md from disk. Point it at `https://mcp.sugra.ai/mcp`.

## Local check

```bash
python scripts/check.py
```

## License

MIT. Data from each endpoint carries its own upstream terms. See https://sugra.ai/sources and per-response `meta`.
